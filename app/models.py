#!/usr/bin/env python
# coding: utf-8

from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# python manager.py shell
# from app.models import User, serverinfo, projectinfo, updatelog
# db.create_all()
# ALTER TABLE projectinfo ADD COLUMN ischeck VARCHAR(10) NULL DEFAULT 'no';

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    _password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)


class serverinfo(db.Model):
    __tablename__ = 'serverinfo'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(64) , index=True)
    hostname = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    variable1 = db.Column(db.String(64))
    variable2 = db.Column(db.String(64))
    variable3 = db.Column(db.String(64))
    variable4 = db.Column(db.String(64))
    variable5 = db.Column(db.String(64))
    variable6 = db.Column(db.String(64))
    variable7 = db.Column(db.String(64))
    variable8 = db.Column(db.String(64))
    variable9 = db.Column(db.String(64))

    def __init__(self, project_name, hostname, ip, variable1, variable2, variable3, variable4, variable5, variable6, variable7, variable8, variable9):
        self.project_name = project_name
        self.hostname = hostname
        self.ip = ip
        self.variable1 = variable1
        self.variable2 = variable2
        self.variable3 = variable3
        self.variable4 = variable4
        self.variable5 = variable5
        self.variable6 = variable6
        self.variable7 = variable7
        self.variable8 = variable8
        self.variable9 = variable9


class userservicegroup(db.Model):
    __tablename__ = 'userservicegroup'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    servicegroup = db.Column(db.String(64))
    permissions = db.Column(db.String(64))

    def __init__(self, username, servicegroup, permissions):
        self.username = username
        self.servicegroup = servicegroup
        self.permissions = permissions

class projectinfo(db.Model):
    __tablename__ = 'projectinfo'
    project_name = db.Column(db.String(64), primary_key=True)
    project = db.Column(db.String(64))
    environment = db.Column(db.String(64))
    branch = db.Column(db.String(64))
    type = db.Column(db.String(50))
    git = db.Column(db.String(1024))
    port = db.Column(db.Integer)
    make = db.Column(db.Text)
    istag = db.Column(db.String(10))
    isnginx = db.Column(db.String(10))
    business = db.Column(db.String(40))
    ischeck = db.Column(db.String(10))
    checkurl = db.Column(db.String(300))
    statuscode = db.Column(db.String(8))

    def __init__(self, project_name, project, environment, branch, type, git, port, make, istag, isnginx, business, ischeck, checkurl, statuscode):
        self.project_name = project_name
        self.project = project
        self.environment = environment
        self.branch = branch
        self.type = type
        self.git = git
        self.port = port
        self.make = make
        self.istag = istag
        self.isnginx = isnginx
        self.business = business
        self.ischeck = ischeck
        self.checkurl = checkurl
        self.statuscode = statuscode


class project_config(db.Model):
    __tablename__ = 'project_config'
    project_name = db.Column(db.String(64), primary_key=True)
    config1 = db.Column(db.Text)
    config2 = db.Column(db.Text)
    config3 = db.Column(db.Text)
    config4 = db.Column(db.Text)
    config5 = db.Column(db.Text)
    config6 = db.Column(db.Text)
    config7 = db.Column(db.Text)
    config8 = db.Column(db.Text)
    config9 = db.Column(db.Text)
    config10 = db.Column(db.Text)

    def __init__(self, project_name, config1, config2, config3, config4, config5, config6, config7, config8, config9, config10):
        self.project_name = project_name
        self.config1 = config1
        self.config2 = config2
        self.config3 = config3
        self.config4 = config4
        self.config5 = config5
        self.config6 = config6
        self.config7 = config7
        self.config8 = config8
        self.config9 = config9
        self.config10 = config10


class updatelog(db.Model):
    __tablename__ = 'updatelog'
    id = db.Column(db.Integer, primary_key=True)
    taskid = db.Column(db.String(64), index=True)
    project_name = db.Column(db.String(64))
    host = db.Column(db.String(2000))
    tag = db.Column(db.String(64))
    rtime = db.Column(db.String(32))
    status = db.Column(db.String(10))
    loginfo = db.Column(db.Text)

    def __init__(self, taskid, project_name, host, tag, rtime, status, loginfo):
        self.taskid = taskid
        self.project_name = project_name
        self.host = host
        self.tag = tag
        self.rtime = rtime
        self.status = status
        self.loginfo = loginfo


class updateoperation(db.Model):
    __tablename__ = 'updateoperation'
    taskid = db.Column(db.String(64), primary_key=True, index=True)
    project_name = db.Column(db.String(64))
    hostlist = db.Column(db.String(2000))
    tag = db.Column(db.String(64))
    rtime = db.Column(db.String(32))
    operation = db.Column(db.String(64))
    loginfo = db.Column(db.String(6400))
    user = db.Column(db.String(50))

    def __init__(self, taskid, project_name, hostlist, tag, rtime, operation, loginfo, user):
        self.taskid = taskid
        self.project_name = project_name
        self.hostlist = hostlist
        self.tag = tag
        self.rtime = rtime
        self.operation = operation
        self.loginfo = loginfo
        self.user = user


class workorder(db.Model):
    __tablename__ = 'workorder'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(64))
    project = db.Column(db.String(64))
    applicant = db.Column(db.String(64))
    applicationtime = db.Column(db.String(64))
    status = db.Column(db.String(64))
    executor = db.Column(db.String(64))
    completiontime = db.Column(db.String(64))
    remarks = db.Column(db.Text)

    def __init__(self, group, project, applicant, applicationtime, status, executor, completiontime, remarks):
        self.group = group
        self.project = project
        self.applicant = applicant
        self.applicationtime = applicationtime
        self.status = status
        self.executor = executor
        self.completiontime = completiontime
        self.remarks = remarks


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

