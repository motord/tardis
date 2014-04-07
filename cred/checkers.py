# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from tornado import gen
import psycopg2
from backends import db


class TenantCredentailsChecker(object):
    def __init__(self):
        super(TenantCredentailsChecker, self).__init__()
        self.query="SELECT tenantname, email, crypted_password, password_salt FROM tenants WHERE email = '{0}'"

    @gen.coroutine
    def requestTenantName(self, credentials):
        try:
            cursor = yield momoko.Op(db.execute, self.query.format(credentials.email))
        except (psycopg2.Warning, psycopg2.Error) as error:
            self.write(str(error))
        else:
            tenantname, email, password, salt=cursor.fetchone()
            if credentials.checkPassword(password, salt):
                raise gen.Return(tenantname)
            raise gen.Return(None)

class AvatarCredentailsChecker(object):
    def __init__(self):
        self.query="SELECT id, email, password_salt, crypted_password FROM avatars WHERE email = '{0}'"

    @gen.coroutine
    def requestAvatarId(self, credentials):
        try:
            cursor = yield momoko.Op(db.execute, self.query.format(credentials.email))
        except (psycopg2.Warning, psycopg2.Error) as error:
            self.write(str(error))
        else:
            id, email, salt, password=cursor.fetchone()
            if credentials.checkPassword(password, salt):
                raise gen.Return(id)
            raise gen.Return(None)
