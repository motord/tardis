# -*- coding: utf-8 -*-
__author__ = 'peter'

from base import HEAD, GET, POST, DELETE, PATCH, PUT, OPTIONS
from base import BaseHandler
from base import SessionRequestHandler
from box import BoxesHandler
from tenant import TenantHandler
from node import NodesHandler
from bot import BotsHandler
from web import LoginHandler, DashboardHandler