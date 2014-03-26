# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
import tornado.template
from handlers.base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

class DashboardHandler(BaseHandler):
    def get(self):
        self.render("index.html")
