#! /usr/bin/env python
import cherrypy
from mako.template import Template
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

class Server(object):

    @cherrypy.expose
    def index(self):
        template = Template(filename=os.path.join(current_dir,'templates/index.html'))
        return template.render()

    @cherrypy.expose
    def analyse(self, text):
        words = text.split()
        pairs = []
        if len(words) > 1:
            pairs = [words[i:i+2] for i in range(0, len(words)-1)]
        else:
            pairs = [words]
        return unicode(pairs)

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
