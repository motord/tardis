# -*- coding: utf-8 -*-
__author__ = 'peter'

import tornado.web
import tornado.escape
from handlers.base import BaseHandler

import logging
LOGGER = logging.getLogger(__name__)


class AvatarHandler(BaseHandler):
    def post(self):
        pass
