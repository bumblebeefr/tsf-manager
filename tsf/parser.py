import re
from wand.image import Image
import tempfile
import os
from wand.color import Color
from wand.drawing import Drawing
import sys
import logging


headers_re = {
    'ProcessMode': re.compile('<ProcessMode: (.*)>'),
    'Size': re.compile('<Size: ([0-9\.]*);([0-9\.]*)>'),
    'MaterialGroup': re.compile('<MaterialGroup: (.*)>'),
    'MaterialName': re.compile('<MaterialName: (.*)>'),
    'JobName': re.compile('<JobName: (.*)>'),
    'JobNumber': re.compile('<JobNumber: ([0-9]*)>'),
    'Resolution': re.compile('<Resolution: ([0-9]*)>'),
    'LayerParameter': re.compile('<LayerParameter: ([0-9]*);([0-9\.]*)>'),
    'StampShoulder': re.compile('<StampShoulder: (.*)>'),
    'Cutline': re.compile('<Cutline: (.*)>'),
}
headers_transfo = {
    'ProcessMode': lambda x: x[0],
    'Size': lambda x: {'width': float(x[0]), 'height': float(x[1])},
    'MaterialGroup': lambda x: x[0],
    'MaterialName': lambda x: x[0],
    'JobName': lambda x: x[0].decode('iso-8859-1'),
    'JobNumber': lambda x: int(x[0]),
    'Resolution': lambda x: int(x[0]),
    'LayerParameter': lambda x: {'layers': int(x[0]), 'adjustment': float(x[1])},
    'StampShoulder': lambda x: x[0],
    'Cutline': lambda x: x[0],
}


bmp_re = re.compile('<STBmp: (.*)>BM(.*)<EOBmp>', re.S)
polygones_re = re.compile('<DrawPolygon: ([0-9;]*)>')

TROTEC_COLORS = [
    '#ff0000',
    '#0000ff',
    '#336699',
    '#00ffff',
    '#00ff00',
    '#009933',
    '#006633',
    '#999933',
    '#996633',
    '#663300',
    '#660066',
    '#9900cc',
    '#ff00ff',
    '#ff6600',
    '#ffff00'
]


def group(t, n):
    return zip(*[t[i::n] for i in range(n)])


def mm2px(dpi, val):
    return int(round(1.0 * val * dpi * 0.0393701))


def hex_color(rgb_tuple):
    hexcolor = '#%02x%02x%02x' % tuple([int(x) for x in rgb_tuple])
    return hexcolor


def draw_polygon(draw, data):
    polygons = data[4:]
    color = data[1:4]
    with Color('rgb(%s,%s,%s)' % tuple(color)) as color:
        draw.fill_color = color
        draw.stroke_width = 4.0
        prev_point = None
        for p in group(polygons, 2):
            if(prev_point is not None):
                draw.line(prev_point, p)
            prev_point = p


def polygon_topath(data):
    polygons = data[4:]
    color = data[1:4]
    path = ['<path style="stroke:%s; fill:none; stroke-width: 3;" ' % hex_color(color), 'd="M']
    for p in group(polygons, 2):
        path.append("%s,%s " % tuple(p))
    path.append('" />')
    return "".join(path)


def get_image(tsf_buff, headers):
    m = bmp_re.search(tsf_buff)
    if(m):
        return Image(blob="BM" + m.group(2))
    else:
        return Image(width=mm2px(headers['Resolution'], headers['Size']['width']), height=mm2px(headers['Resolution'], headers['Size']['height']))


def get_base64_img(tsf_buff, headers):
    m = bmp_re.search(tsf_buff)
    if(m):
        with Image(blob="BM" + m.group(2)) as img:
            img.flip()
            img.transform(resize='1920x1080>')
            img.format = 'jpg'
            return img.make_blob().encode("base64").replace('\n', '')
    else:
        None


def parse_headers(tsf_file):
    try:
        with open(tsf_file, "r") as f:
            tsf_buff = f.read()

            headers = {}
            for k in headers_re:
                if(headers_re[k].search(tsf_buff)):
                    headers[k] = headers_transfo[k](headers_re[k].search(tsf_buff).groups())

            headers['px_width'] = mm2px(headers['Resolution'], headers['Size']['width'])
            headers['px_height'] = mm2px(headers['Resolution'], headers['Size']['height'])
            headers['bmp'] = False

            if(bmp_re.search(tsf_buff)):
                headers['bmp'] = True

            colors = set()
            for p in polygones_re.findall(tsf_buff):
                colors.add(hex_color(p.split(';')[1:4]))

            headers['cut'] = list(colors)

            headers['valid'] = True
            return headers
    except Exception:
        logging.exception("Error loading headers for %s" % tsf_file)
        return {"valid": False}


def parse_headers2(tsf_file):
    try:
        with open(tsf_file, "r") as file:
            headers = {
                'ProcessMode': None,
                'Size': {'width': 0, 'height': 0},
                'MaterialGroup': None,
                'MaterialName': None,
                'JobName': None,
                'JobNumber': 0,
                'Resolution': 300,
                'LayerParameter': {'layers': 1, 'adjustment': 0},
                'StampShoulder': None,
                'Cutline': [],
            }
            headers['bmp'] = False
            colors = set()
            if(tsf_file.endswith(".tsf")):
                for line in file:
                    for k in headers_re:
                        found = headers_re[k].search(line)
                        if(found):
                            headers[k] = headers_transfo[k](found.groups())
                            break

                    if line.find('<BegGroup: Bitmap>') > -1:
                        headers['bmp'] = True

                    for p in polygones_re.findall(line):
                        colors.add(hex_color(p.split(';')[1:4]))

                headers['px_width'] = mm2px(headers['Resolution'], headers['Size']['width'])
                headers['px_height'] = mm2px(headers['Resolution'], headers['Size']['height'])
                headers['valid'] = True

            headers['cut'] = [k for k in TROTEC_COLORS if k in colors]
            return headers
    except Exception:
        logging.exception("Error loading headers for %s" % tsf_file)
        return {"valid": False}

# deprecated won't work anymore


def extract_preview(tsf_file, headers):
    try:
        fd, fp = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        logging.debug(extract_svg(tsf_file, headers))
        with open(tsf_file, "r") as f:
            tsf_buff = f.read()
            with get_image(tsf_buff, headers) as img:
                img.flip()
                with Drawing() as draw:
                    for p in polygones_re.findall(tsf_buff):
                        draw_polygon(draw, p.split(';'))
                    draw(img)

                img.transform(resize='1920x1080>')
                img.format = 'png'
                img.save(filename=fp)
        return fp
    except Exception:
        logging.exception("Error extracting preview for %s" % tsf_file)
        return None


def extract_preview2(tsf_file, headers, svg_path, jpg_path):
    #logging.debug(extract_svg(tsf_file, headers))
    engrave_img = None
    try:
        with open(tsf_file, "r") as f:
            tsf_buff = f.read()
            engrave_img = get_base64_img(tsf_buff, headers)

    except Exception:
        logging.exception("Error extracting preview for %s" % tsf_file)

    with open(svg_path, "w+") as svg_file:
        svg_file.write(extract_svg(tsf_file, headers, engrave_img))


def extract_svg(tsf_file, headers, engrave_img=None):
    with open(tsf_file, "r") as f:
        tsf_buff = f.read()
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%s" height="%s" viewBox="0 0 %s %s" >' % (headers.get("px_width"), headers.get("px_height"), headers.get("px_width"), headers.get("px_height"))]
        if(engrave_img):
            # with open(jpg_path, "rb") as img:
                #svg.append('<image x="0" y="0" width="%s" height="%s" xlink:href="data:image/jpg;base64,%s" />' % (headers.get("px_width"), headers.get("px_height"), img.read().encode("base64").replace('\n', '')))
            svg.append('<image x="0" y="0" width="%s" height="%s" xlink:href="data:image/jpg;base64,%s" />' % (headers.get("px_width"), headers.get("px_height"), engrave_img))
        for p in polygones_re.findall(tsf_buff):
            svg.append(polygon_topath(p.split(';')))
        svg.append("</svg>")
    return "\n".join(svg)

if __name__ == '__main__':
    print parse_headers(sys.argv[1])
