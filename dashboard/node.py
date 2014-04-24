# -*- coding: utf-8 -*-
__author__ = 'peter'

from handlers.avatar import AvatarRequestHandler


class NodesHandler(AvatarRequestHandler):
    def get(self, collection, id):
        pass