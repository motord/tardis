# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from model import AsyncModel
import mopee
from tornado import gen
from box import Box


class Bot(AsyncModel):
    id= mopee.UUIDField(primary_key=True)
    box=mopee.ForeignKeyField(Box, related_name='bots')
    name=mopee.CharField()
    leverage=mopee.TextField()
    created_at= mopee.DateTimeField
    updated_at= mopee.DateTimeField()

    class Meta:
        db_table='bots'
