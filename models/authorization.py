# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from model import AsyncModel
import mopee
from tornado import gen
from avatar import Avatar


class Authorization(AsyncModel):
    id= mopee.IntegerField(primary_key=True)
    access_token=mopee.CharField()
    refresh_token=mopee.TextField()
    expires_at= mopee.DateTimeField()
    scope= mopee.TextField()
    origin= mopee.CharField()
    avatar=mopee.ForeignKeyField(Avatar, related_name='authorizations')
    created_at= mopee.DateTimeField
    updated_at= mopee.DateTimeField()

    class Meta:
        db_table='authorizations'
