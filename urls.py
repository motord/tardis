# -*- coding: utf-8 -*-
__author__ = 'peter'

from handlers import BoxesHandler, TenantHandler, LoginHandler, DashboardHandler

url_patterns = [
    (r"/", DashboardHandler),
    (r"/login", LoginHandler),
    (r"/boxes", BoxesHandler),
]