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
from decorators import tenant_authenticated

import logging
LOGGER = logging.getLogger(__name__)


class LoginHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)
        self.checker = TenantCredentailsChecker(self.db)

    def get(self):
        self.render("login.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        credentials= TenantEmailPassword(self.get_argument("email"), self.get_argument("password"))
        tenantname=yield self.checker.requestTenantName(credentials)
        if tenantname:
            self.set_secure_cookie("tenantname", tenantname)
            self.redirect('/')


class RegistrationHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        salt = uuid.uuid4().hex
        # hash = hashlib.sha512(password + salt).hexdigest()
        self.render("login.html")

class DashboardHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tenant_authenticated
    def get(self):
        self.render("index.html", tenant=self.current_tenant)
