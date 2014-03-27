# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
import tornado.template
from base import BaseHandler

import logging
LOGGER = logging.getLogger(__name__)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

class DashboardHandler(BaseHandler):
    def get(self):
        self.render("index.html")
