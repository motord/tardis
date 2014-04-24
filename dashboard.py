# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options
import momoko

from settings import settings
from dashboard import BoxesHandler, LoginHandler, DashboardHandler, BotsHandler, NodesHandler

url_patterns = [
    (r"/", DashboardHandler),
    (r"/login", LoginHandler),
    (r"/boxes", BoxesHandler),
    (r"/bots", BotsHandler),
    (r"/classes/([a-z]+)", NodesHandler),
    (r"/classes/([a-z]+)/([0-9]+)", NodesHandler),
]

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()