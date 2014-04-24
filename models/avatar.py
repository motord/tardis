# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from model import AsyncModel
import mopee
from tornado import gen
from box import Box


class Avatar(AsyncModel):
    id= mopee.IntegerField(primary_key=True)
    box=mopee.ForeignKeyField(Box, related_name='avatars')
    login=mopee.CharField()
    email=mopee.TextField()
    desc=mopee.TextField()
    crypted_password= mopee.CharField()
    password_salt= mopee.CharField()
    login_count=mopee.IntegerField()
    last_request_at=mopee.DateTimeField()
    last_login_at=mopee.DateTimeField()
    current_login_at=mopee.DateTimeField()
    last_login_ip=mopee.CharField()
    current_login_ip=mopee.CharField()
    created_at= mopee.DateTimeField
    updated_at= mopee.DateTimeField()

    class Meta:
        db_table='avatars'
