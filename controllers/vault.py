# -*- coding: utf-8 -*-
__author__ = 'peter'

from .. import app
from bottle import template, request


@app.route('/', method='GET')
def index():
    return template('vault', message='')


# @app.route('/print', method=['GET', 'POST'])
# def printer():
#     if request.method == 'POST':
#         from ..models.Printer import Printer
#         printer = Printer()
#         message = printer.show_string(request.forms.get('text'))
#         return template('printer/index', message=message)
#     return template('printer/print', message='')