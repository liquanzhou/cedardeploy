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
    pnum = db.Column(db.String(32))
    env = db.Column(db.String(3200))
    checkstatus = db.Column(db.String(64))
    checktime = db.Column(db.String(64))
    commitid = db.Column(db.String(64))
    updatestatus = db.Column(db.String(64))
    updatetime = db.Column(db.String(64))

    def __init__(self, project_name, hostname, ip, pnum, env, checkstatus, checktime, commitid, updatestatus, updatetime):
        self.project_name = project_name
        self.hostname = hostname
        self.ip = ip
        self.pnum = pnum
        self.env = env
        self.checkstatus = checkstatus
        self.checktime = checktime
        self.commitid = commitid
        self.updatestatus = updatestatus
        self.updatetime = updatetime


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
    business = db.Column(db.String(40))
    environment = db.Column(db.String(64))
    project = db.Column(db.String(64))
    type = db.Column(db.String(50))
    port = db.Column(db.Integer)
    git = db.Column(db.String(1024))
    branch = db.Column(db.String(64))


    def __init__(self, project_name, business, environment, project, type, port, git, branch):
        self.project_name = project_name
        self.business = business
        self.environment = environment
        self.project = project
        self.type = type
        self.port = port
        self.git = git
        self.branch = branch


class project_config(db.Model):
    __tablename__ = 'project_config'
    project_name = db.Column(db.String(64), primary_key=True)
    make = db.Column(db.Text)
    supervisor = db.Column(db.Text)
    config = db.Column(db.Text)
    remarks = db.Column(db.Text)
    startcmd = db.Column(db.String(200))
    packfile = db.Column(db.String(200))
    istag = db.Column(db.String(10))
    checkport = db.Column(db.String(10))
    checkhttp = db.Column(db.String(10))
    httpurl = db.Column(db.String(2000))
    httpcode = db.Column(db.String(8))


    def __init__(self, project_name, make, supervisor, config, remarks, startcmd, packfile, istag, checkport, checkhttp, httpurl, httpcode):
        self.project_name = project_name
        self.make = make
        self.supervisor = supervisor
        self.config = config
        self.remarks = remarks
        self.startcmd = startcmd
        self.packfile = packfile
        self.istag = istag
        self.checkport = checkport
        self.checkhttp = checkhttp 
        self.httpurl = httpurl
        self.httpcode = httpcode


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
    user = db.Column(db.String(50))
    status = db.Column(db.String(20))
    commitid = db.Column(db.String(1024))

    def __init__(self, taskid, project_name, hostlist, tag, rtime, operation, user, status, commitid):
        self.taskid = taskid
        self.project_name = project_name
        self.hostlist = hostlist
        self.tag = tag
        self.rtime = rtime
        self.operation = operation
        self.user = user
        self.status = status
        self.commitid = commitid


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

