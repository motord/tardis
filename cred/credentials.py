# -*- coding: utf-8 -*-
__author__ = 'peter'

import hashlib


class TenantEmailPassword:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def checkPassword(self, password, salt):
        return hashlib.sha512(self.password + salt).hexdigest() == password


class AvatarEmailPasswordBoxId:

    def __init__(self, email, password, box_id):
        self.email = email
        self.password = password
        self.box_id = box_id

    def checkPassword(self, password, salt):
        return hashlib.sha512(self.password + salt).hexdigest() == password


class BoxIdKey:

    def __init__(self, id, api_key):
        self.id = id
        self.key = api_key

    def checkApiKey(self, api_key):
        return self.key == api_key

    def checkMasterKey(self, master_key):
        return self.key  == master_key
