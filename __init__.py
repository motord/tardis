# -*- coding: utf-8 -*-
__author__ = 'peter'
__version__ = '0.1'

from bottle import Bottle
app = Bottle()
app.catchall = False
from controllers import *
