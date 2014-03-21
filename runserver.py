# -*- coding: utf-8 -*-
__author__ = 'peter'

import os
from tardis import app
from bottle import debug, run

import bottle
bottle.TEMPLATE_PATH.insert(0,'/home/peter/Projects/tardis/views/')

debug(True)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    run(app, reloader=True, host='0.0.0.0', port=port)