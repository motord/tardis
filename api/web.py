# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
import tornado.template
import tornado.gen
from handlers.avatar import AvatarRequestHandler
import uuid
import hashlib
from cred import AvatarEmailPasswordBoxId, AvatarCredentailsChecker

import logging
LOGGER = logging.getLogger(__name__)


class LoginHandler(AvatarRequestHandler):
    def __init__(self, application, request, **kwargs):
        super(LoginHandler, self).__init__(application, request, **kwargs)
        self.checker = AvatarCredentailsChecker()

    def get(self):
        self.render("login.html")

    @tornado.gen.coroutine
    def post(self):
        credentials= AvatarEmailPasswordBoxId(self.get_argument("email"), self.get_argument("password"))
        avatar=yield tornado.gen.Task(self.checker.requestAvatar, credentials)
        if avatar:
            self.set_secure_cookie("avatarid", avatar.id)
            self.redirect('/')


class RegistrationHandler(AvatarRequestHandler):
    def get(self):
        self.render("register.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        salt = uuid.uuid4().hex
        # hash = hashlib.sha512(password + salt).hexdigest()
        self.render("login.html")