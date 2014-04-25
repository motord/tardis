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


class BoxClientIdClientSecret:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def checkApiKey(self, api_key):
        return self.client_secret == api_key

    def checkMasterKey(self, master_key):
        return self.client_secret  == master_key
