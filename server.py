#! /usr/bin/env python
import cherrypy
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

class Server(object):

    @cherrypy.expose
    def index(self):
        return 'hello world'

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
