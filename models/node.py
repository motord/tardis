# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from model import AsyncModel
import mopee
from tornado import gen
from box import Box
from avatar import Avatar


class Node(AsyncModel):
    id= mopee.IntegerField(primary_key=True)
    box=mopee.ForeignKeyField(Box, related_name='nodes')
    collection= mopee.CharField()
    data= mopee.JSONField()
    updated_at= mopee.DateTimeField()
    avatar= mopee.ForeignKeyField(Avatar, related_name='nodes')

    class Meta:
        db_table='nodes'
