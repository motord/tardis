# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from tornado import gen
import psycopg2
from backends import db
from models import Box, Tenant, Avatar


class TenantCredentailsChecker(object):
    def __init__(self):
        self.query="SELECT tenantname, email, crypted_password, password_salt FROM tenants WHERE email = '{0}'"

    @gen.coroutine
    def requestTenant(self, credentials):
        tenant=yield gen.Task(Tenant.select().where(Tenant.email == credentials.email).get)
        # try:
        #     cursor = yield momoko.Op(db.execute, self.query.format(credentials.email))
        # except (psycopg2.Warning, psycopg2.Error) as error:
        #     self.write(str(error))
        # else:
        #     tenantname, email, password, salt=cursor.fetchone()
        #     if credentials.checkPassword(password, salt):
        #         raise gen.Return(tenantname)
        #     raise gen.Return(None)
        if credentials.checkPassword(tenant.crypted_password, tenant.password_salt):
            raise gen.Return(tenant)
        raise gen.Return(None)

class AvatarCredentailsChecker(object):
    def __init__(self):
        self.query="SELECT id, email, password_salt, crypted_password FROM avatars WHERE email = '{0}' AND box_id = {1}"

    @gen.coroutine
    def requestAvatar(self, credentials):
        avatar=yield gen.Task(Avatar.select().where((Avatar.email == credentials.email) & (Avatar.box.id==credentials.box_id)).get)
        # try:
        #     cursor = yield momoko.Op(db.execute, self.query.format(credentials.email, credentials.box_id))
        # except (psycopg2.Warning, psycopg2.Error) as error:
        #     self.write(str(error))
        # else:
        #     id, email, salt, password=cursor.fetchone()
        #     if credentials.checkPassword(password, salt):
        #         raise gen.Return(id)
        #     raise gen.Return(None)
        if credentials.checkPassword(avatar.crypted_password, avatar.password_salt):
            raise gen.Return(avatar)
        raise gen.Return(None)


class BoxCredentialsChecker(object):
    def __init__(self):
        self.query="SELECT id, api_key, master_key FROM boxes WHERE id = '{0}'"

    @gen.coroutine
    def requestBox(self, credentials):
        box=yield gen.Task(Box.select().where(Box.client_id==credentials.client_id).get)
        # try:
        #     cursor = yield momoko.Op(db.execute, self.query.format(credentials.client_id))
        # except (psycopg2.Warning, psycopg2.Error) as error:
        #     self.write(str(error))
        # else:
        #     id, api_key, master_key=cursor.fetchone()
        #     if credentials.checkApiKey(api_key):
        #         raise gen.Return(id)
        #     if credentials.checkMasterKey(master_key):
        #         raise gen.Return(id)
        #     raise gen.Return(None)
        if credentials.checkApiKey(box.api_key):
            raise gen.Return(box)
        if credentials.checkMasterKey(box.master_key):
            raise gen.Return(box)
        raise gen.Return(None)
