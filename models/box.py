# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from model import AsyncModel
import mopee
from tornado import gen
from tenant import Tenant


class Box(AsyncModel):
    id= mopee.UUIDField(primary_key=True)
    name=mopee.CharField()
    desc=mopee.TextField()
    start_url= mopee.CharField()
    icon_url= mopee.CharField()
    website_url= mopee.CharField()
    api_key= mopee.CharField()
    master_key= mopee.CharField()
    tenant=mopee.ForeignKeyField(Tenant, related_name='boxes')
    created_at= mopee.DateTimeField
    updated_at= mopee.DateTimeField()

    class Meta:
        db_table='boxes'
