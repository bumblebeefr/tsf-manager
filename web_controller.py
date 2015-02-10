#! /usr/bin/env python
# -*- encoding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session,send_file, Response
import logging
import os
from os import path
import tsf
from sse import Publisher
from datetime import datetime
from pyinotify import WatchManager, ThreadedNotifier, ProcessEvent
import pyinotify

HOST = '0.0.0.0'
PORT = 4242
from local_settings import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'poezrunç_-xqhmdhc:xqhm!,nvuqmvlfugsbl;:*'

# publisher = Publisher()
# wm = WatchManager()
# mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE  # watched events


# class PTmp(ProcessEvent):
#     def process_IN_CREATE(self, event):
#         print "Create: %s" %  os.path.join(event.path, event.name)
#         publisher.publish("Create: %s" %  os.path.join(event.path, event.name))
# 
#     def process_IN_DELETE(self, event):
#         print "Remove: %s" %  os.path.join(event.path, event.name)
#         publisher.publish("Remove: %s" %  os.path.join(event.path, event.name))
# 
#     def IN_CLOSE_WRITE(self, event):
#         print "Modification: %s" %  os.path.join(event.path, event.name)
#         publisher.publish("Modification: %s" %  os.path.join(event.path, event.name))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# @app.route('/msg', methods=['GET'])
# def msg():
#     publisher.publish('New visit at {}!'.format(datetime.now()))
#     return "OK"


@app.route('/spool/list.json', methods=['GET'])
def spool_list():
    #TODO see os.walk
    tsf_list = []
    for f in os.listdir(SPOOL_DIR):
        tsf_file = tsf.TsfFile(os.path.join(SPOOL_DIR, f))
        tsf_list.append(tsf_file.to_dict())

    return jsonify(tsf_list=tsf_list)


@app.route('/tsf/directpreview/<path:preview_path>.jpg')
def preview_file(preview_path):
    preview = path.join(PREVIEW_DIR, "%s.png" % preview_path)
    return send_file(preview, mimetype="image/jpg")


@app.route('/tsf/preview/<path:tsf_path>.svg')
def tsf_preview(tsf_path):
    tsf_file = tsf.TsfFile(os.path.join(BASE_DIR, tsf_path))
    return send_file(tsf_file.preview(), mimetype="image/svg+xml")


# @app.route('/subscribe')
# def subscribe():
#     return Response(publisher.subscribe(), content_type='text/event-stream')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='\033[1;30m%(asctime)s \033[0;33m%(levelname)s \033[0m%(module)s:%(lineno)-4s \033[1;32m%(threadName)s:%(funcName)s \033[0m%(message)s\033[0m')
    logging.info("Starting")

#     notifier = ThreadedNotifier(wm, PTmp())
#     notifier.setDaemon(True)
#     notifier.start()
#     wdd = wm.add_watch(BASE_DIR, mask, rec=True)

    app.run(host=HOST, port=PORT, threaded=True, debug=True)


