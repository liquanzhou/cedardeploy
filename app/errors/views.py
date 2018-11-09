#!/usr/bin/env python
# coding: utf-8

from flask import render_template
from . import errors

#@errors.errorhandler(404)
#def test(e):
#    return "test"

@errors.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
