# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
from handlers.tenant import TenantRequestHandler

class BoxesHandler(TenantRequestHandler):
    def get(self):
        pass

    def post(self):
        pass