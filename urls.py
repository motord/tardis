# -*- coding: utf-8 -*-
__author__ = 'peter'

from handlers import BoxHandler, TenantHandler, LoginHandler, DashboardHandler

url_patterns = [
    (r"/", DashboardHandler),
    (r"/login", LoginHandler),
]