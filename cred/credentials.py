# -*- coding: utf-8 -*-
__author__ = 'peter'

import hashlib


class TenantEmailPassword:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def checkPassword(self, password, salt):
        return hashlib.sha512(self.password + salt).hexdigest() == password


class AvatarEmailPassword:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def checkPassword(self, password, salt):
        return hashlib.sha512(self.password + salt).hexdigest() == password
