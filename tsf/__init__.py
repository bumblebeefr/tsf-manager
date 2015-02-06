from local_settings import *
from os import path
import hashlib
from datetime import datetime
import simplejson
import os
import shutil
import errno
import logging

from tsf import parser


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def str_weight(weight):
    i = 0
    while weight > 1024:
        weight = 1.0 * weight / 1024
        i += 1
    logging.debug(weight)
    return "%0.1f%s" % (weight, ("o", "Ko", "Mo", "Go", "To")[i])


class TsfFile:

    def __init__(self, full_path):
        if not path.isfile(full_path):
            raise Exception("%s is not a file" % full_path)

        self.full_path = full_path
        self.directory, self.filename = path.split(self.full_path)
        self.directory = self.directory.replace(BASE_DIR, '')
        self.name = self.filename.replace(".tsf", "")
        self._checksum = None
        self._headers = None
        self.creation_date = datetime.fromtimestamp(path.getctime(full_path))
        self.modification_date = datetime.fromtimestamp(path.getmtime(full_path))
        self.size = path.getsize(full_path)

    def checksum_md5(self):
        if not self._checksum:
            md5 = hashlib.md5()
            with open(self.full_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            self._checksum = md5.hexdigest()
        return self._checksum

    def to_dict(self):
        return {
            'directory': self.directory,
            'filename': self.filename,
            'checksum': self.checksum_md5(),
            'headers': self.headers(),
            'date': self.creation_date.isoformat(),
            'weight': self.size,
            'sweight': str_weight(self.size)
        }

    def headers(self):
        if self._headers is None:
            header_file = path.join(PREVIEW_DIR, "%s/%s-%s.json" % (self.creation_date.strftime("%Y-%m-%d"), self.name, self.checksum_md5()))
            if path.isfile(header_file):
                with open(header_file) as f:
                    self._headers = simplejson.load(f)
            else:
                self._headers = parser.parse_headers2(self.full_path)
                mkdir(path.join(PREVIEW_DIR, self.creation_date.strftime("%Y-%m-%d")))
                with open(header_file, 'w+') as f:
                    simplejson.dump(self._headers, f)

        return self._headers

    def preview(self):
        preview_svg = path.join(PREVIEW_DIR, "%s/%s-%s.svg" % (self.creation_date.strftime("%Y-%m-%d"), self.name, self.checksum_md5()))
        preview_jpg = path.join(PREVIEW_DIR, "%s/%s-%s.jpg" % (self.creation_date.strftime("%Y-%m-%d"), self.name, self.checksum_md5()))

        if not path.isfile(preview_svg):
            mkdir(path.join(PREVIEW_DIR, self.creation_date.strftime("%Y-%m-%d")))
            parser.extract_preview2(self.full_path, self.headers(), preview_svg, preview_jpg)

        logging.debug("preview : %s" % preview_svg)
        return preview_svg

#         preview_file = path.join(PREVIEW_DIR, "%s/%s-%s.png" % (self.creation_date.strftime("%Y-%m-%d"), self.name, self.checksum_md5()))
#         if not path.isfile(preview_file):
#             mkdir(path.join(PREVIEW_DIR, self.creation_date.strftime("%Y-%m-%d")))
#             tmp = parser.extract_preview(self.full_path, self.headers())
#             if(tmp):
#                 shutil.move(tmp, preview_file)
#         return preview_file
