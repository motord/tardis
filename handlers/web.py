# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
import tornado.template
import tornado.gen
from base import TenantRequestHandler
import uuid
import hashlib
from cred import TenantEmailPassword, TenantCredentailsChecker
from decorators import tenant_authenticated

import logging
LOGGER = logging.getLogger(__name__)


class LoginHandler(TenantRequestHandler):
    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)
        self.checker = TenantCredentailsChecker()

    def get(self):
        self.render("login.html")

    @tornado.gen.coroutine
    def post(self):
        credentials= TenantEmailPassword(self.get_argument("email"), self.get_argument("password"))
        tenantname=yield tornado.gen.Task(self.checker.requestTenantName, credentials)
        if tenantname:
            self.set_secure_cookie("tenantname", tenantname)
            self.redirect('/')


class RegistrationHandler(TenantRequestHandler):
    def get(self):
        self.render("register.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        salt = uuid.uuid4().hex
        # hash = hashlib.sha512(password + salt).hexdigest()
        self.render("login.html")

class DashboardHandler(TenantRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    @tenant_authenticated
    def get(self):
        self.render("index.html", tenantname=self.current_tenant)
