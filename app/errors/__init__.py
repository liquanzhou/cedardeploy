#!/usr/bin/env python
# coding: utf-8

from flask import Blueprint

errors = Blueprint('errors', __name__)

from . import views
