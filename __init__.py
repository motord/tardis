# -*- coding: utf-8 -*-
__author__ = 'peter'
__version__ = '0.1'


from cork import Cork
from cork.backends import SqlAlchemyBackend
from patches import SqlAlchemyBackendInitializer

# sai = SqlAlchemyBackendInitializer('postgresql+psycopg2://peter:omerta@localhost/knuckle')
sa = SqlAlchemyBackend('postgresql+psycopg2://peter:omerta@localhost/knuckle')
spigot = Cork(backend=sa)

from bottle import Bottle
app = Bottle()
from controllers import *