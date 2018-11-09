#!/usr/bin/env python
# coding: utf-8

import os
import sys
import datetime
join = os.path.join
basedir = os.path.abspath(os.path.dirname(__file__))

from configdb import *

class Flask_Config():
    SECRET_KEY = 'hI0OkyjTVKBGPnKC'
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s?charset=%s' % (user, passwd, host, port, dbname, charset)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=300)
