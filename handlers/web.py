# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
import tornado.template
import tornado.gen
from base import BaseHandler
import uuid
import hashlib
from cred import TenantEmailPassword, TenantCredentailsChecker

import logging
LOGGER = logging.getLogger(__name__)


class LoginHandler(BaseHandler):
    def __init__(self):
        super(LoginHandler, self).__init__()
        self.checker = TenantCredentailsChecker(self.db)

    def get(self):
        self.render("login.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        # if user["hash"] == hashlib.sha512(password + user["salt"]).hexdigest():
        credentials= TenantEmailPassword(self.get_argument("email"), self.get_argument("password"))
        tenantname=self.checker.requestTenantName(credentials)
        if tenantname:
            self.render("index.html")
        self.finish()


class RegistrationHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        salt = uuid.uuid4().hex
        # hash = hashlib.sha512(password + salt).hexdigest()
        self.render("login.html")
        self.finish()

class DashboardHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.render("index.html")
        self.finish()
