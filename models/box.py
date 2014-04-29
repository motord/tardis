# -*- coding: utf-8 -*-
__author__ = 'peter'

import momoko
from model import AsyncModel
import mopee
from tornado import gen
from tenant import Tenant


class Box(AsyncModel):
    client_id= mopee.UUIDField(primary_key=True, db_column='id')
    name=mopee.CharField()
    desc=mopee.TextField()
    start_url= mopee.CharField()
    icon_url= mopee.CharField()
    website_url= mopee.CharField()
    api_key= mopee.CharField()
    master_key= mopee.CharField()
    tenant=mopee.ForeignKeyField(Tenant, related_name='boxes', db_column='tenantname')
    created_at= mopee.DateTimeField
    updated_at= mopee.DateTimeField()

    class Meta:
        db_table='boxes'
