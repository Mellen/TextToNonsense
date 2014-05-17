#! /usr/bin/env python
import cherrypy
from mako.template import Template
import os
import sha
import struct
import math
from difflib import SequenceMatcher
import json
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket
from mysocket import MySocket
import urllib2
import threading
import time
import re
from BeautifulSoup import BeautifulSoup

WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

current_dir = os.path.dirname(os.path.abspath(__file__))

class Server(object):

    def __init__(self):
        cherrypy.engine.subscribe('stop', self.stopPollingTwitter)
        self.lastText = None
        self.diff = 0.0
        self.wsHandlers = []
        self.twitterThread = None
        self.pollingTwitter = False

    def pollTwitter(self):
        exp = re.compile('.*tweet-text.*')
        while self.pollingTwitter:
            failed = False
            i = 0
            try:
                response = urllib2.urlopen('https://twitter.com/search?q=%23random')
            except urllib2.URLError as e:
                cherrypy.log('Cannot read twitter: ' +  str(e.reason))
                failed = True
            if not failed:
                html = response.read()
                soup = BeautifulSoup(html)
                text = soup.find('p', {'class': exp}).text
                self.analyse(text)
            else:
                i = 58
            while self.pollingTwitter and i < 60:
                time.sleep(1)
                i = i + 1

    def stopPollingTwitter(self):
        self.pollingTwitter = False
        self.twitterThread.join()

    def startPollingTwitter(self):
        self.twitterThread = threading.Thread(target=self.pollTwitter)
        self.pollingTwitter = True
        self.twitterThread.demon = True
        self.twitterThread.start()

    @cherrypy.expose
    def index(self):
        template = Template(filename=os.path.join(current_dir,'templates/index.html'))
        return template.render()

    @cherrypy.expose
    def analyse(self, text):
        s1 = sha.new(text.encode('raw_unicode_escape'))
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
            self.diff = 1 - sm.ratio()

        self.lastText = text

        response = json.dumps({'text':text, 'colours':(c1, c2, c3, c4, c5, c6), 'ratio':self.diff})
        
        for handler in self.wsHandlers:
            handler.send(response);
        
        return response

    @cherrypy.expose
    def ws(self):
        cherrypy.request.ws_handler.callback = self.removeHandler
        self.wsHandlers.append(cherrypy.request.ws_handler)

    def removeHandler(self, handler):
        self.wsHandlers.remove(handler)

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
        },
    '/ws': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': MySocket
        }
}

s = Server()

s.startPollingTwitter()

cherrypy.quickstart(s, '/', conf)
