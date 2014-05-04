#! /usr/bin/env python
import cherrypy
from mako.template import Template
import os
import sha
import struct
import math
from difflib import SequenceMatcher
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

class Server(object):

    def __init__(self):
        self.lastText = None
        self.diff = 0.0

    @cherrypy.expose
    def index(self):
        template = Template(filename=os.path.join(current_dir,'templates/index.html'))
        return template.render()

    @cherrypy.expose
    def analyse(self, text):
        s1 = sha.new(text)
        digest = s1.digest()
        bs = bytearray(digest)

        c1 = [b for b in bs[0:3]]
        c2 = [b for b in bs[3:6]]
        c3 = [b for b in bs[6:9]]
        c4 = [b for b in bs[9:12]]
        c5 = [b for b in bs[12:15]]
        c6 = [b for b in bs[15:18]]

        if(self.lastText != None):
            sm = SequenceMatcher(None, text, self.lastText)
            self.diff = 1 - sm.ratio

        self.lastText = text

        return json.dumps((text, (c1, c2, c3, c4, c5, c6), self.diff))

conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        },
    '/js':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'js'),
        },
    '/css':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'css'),
        },
    '/img':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'img'),
        }
}

cherrypy.quickstart(Server(), '/', conf)
