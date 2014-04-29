# -*- coding: utf-8 -*-
__author__ = 'peter'

import uuid
import logging

import tornado.web
import tornado.escape
import tornado.template
import tornado.gen

from handlers.tenant import TenantRequestHandler
from cred import TenantEmailPassword, TenantCredentailsChecker
from decorators import tenant_authenticated

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
        tenant=yield tornado.gen.Task(self.checker.requestTenant, credentials)
        if tenant:
            self.set_secure_cookie("tenantname", tenant.tenantname)
            self.redirect('/')


class RegistrationHandler(TenantRequestHandler):
    def get(self):
        self.render("register.html")

    @tornado.gen.coroutine
    def post(self):
        salt = uuid.uuid4().hex
        # hash = hashlib.sha512(password + salt).hexdigest()
        self.render("login.html")

class DashboardHandler(TenantRequestHandler):
    @tenant_authenticated
    def get(self):
        self.render("index.html", tenantname=self.current_tenant)
