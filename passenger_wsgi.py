# -*- coding: utf-8 -*-
__author__ = 'peter'

import os
import sys

INTERP = "/home/peter/projects/tardis/bin/python"
#INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

nginx_configuration = os.path.dirname(__file__)
project = os.path.dirname(nginx_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

import bottle

def application(environment, response):
  return bottle.default_app.wsgi(environment, response)