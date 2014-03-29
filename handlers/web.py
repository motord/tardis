# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
import tornado.template
from base import BaseHandler
import uuid
import hashlib

import logging
LOGGER = logging.getLogger(__name__)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        # if user["hash"] == hashlib.sha512(password + user["salt"]).hexdigest():
        self.render("login.html")


class RegistrationHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        salt = uuid.uuid4().hex
        # hash = hashlib.sha512(password + salt).hexdigest()
        self.render("login.html")

class DashboardHandler(BaseHandler):
    def get(self):
        self.render("index.html")
