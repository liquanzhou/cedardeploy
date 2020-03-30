#!/usr/bin/env python
# coding: utf-8

import logging
import json
import time
import sys
import os
import subprocess
import datetime
import requests
import socket
import commands
import random
import cPickle
from flask import render_template, request,  session, url_for, redirect, flash
from flask_login import login_required, current_user
from . import main
from ..models import * 
from ..config import *
from .forms import *


reload(sys);
sys.setdefaultencoding('utf8');

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='%s/cedardeploy.log' %path_log,
                filemode='a')


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('online.html')


@main.route("/online", methods=["GET", "POST"])
@login_required
def online():
        return render_template("online.html")


@main.route("/project_admin", methods=["GET", "POST"])
@login_required
def project_admin():
        return render_template("project_admin.html")


@main.route("/online_log", methods=["GET", "POST"])
@login_required
def online_log():
        return render_template("online_log.html")


@main.route("/statistics", methods=["GET", "POST"])
@login_required
def statistics():
        return render_template("statistics.html")


@main.route("/workorderweb", methods=["GET", "POST"])
@login_required
def workorderweb():
        return render_template("workorder.html")

@main.route("/hostlisterrweb", methods=["GET", "POST"])
@login_required
def hostlisterrweb():
        return render_template("hostlisterrweb.html")

@main.route("/hostmanage", methods=["GET", "POST"])
@login_required
def hostmanage():
        return render_template("hostmanage.html")

@main.route("/assets", methods=["GET", "POST"])
@login_required
def assets():
        return render_template("assets.html")

@main.route("/useradmin", methods=["GET", "POST"])
@login_required
def useradmin():
        return render_template("useradmin.html")


@main.route("/portadmin", methods=["GET", "POST"])
@login_required
def portadmin():
        return render_template("portadmin.html")


@main.route("/del_project", methods=["POST"])
@login_required
def del_project():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project = request.form.get('project', 'null')
        if project == 'null':
            raise Exception('ERROR: project null')
        DIR = getdir(project)
        ones = serverinfo.query.filter(serverinfo.project_name == project).all()
        if len(ones) != 0:
            raise Exception('ERROR: Please delete the host.')

        serverinfo.query.filter(serverinfo.project_name == project).delete()
        projectinfo.query.filter(projectinfo.project_name == project).delete()
        project_config.query.filter(project_config.project_name == project).delete()
        os.popen('mv %s %s.%s.del' %(DIR['git'], DIR['git'], time.strftime('%Y%m%d_%H%M'))).read()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/project", methods=["GET", "POST"])
@login_required
def project():

    user = request.args.get("user", "null")
    if user == "null":
        user = current_user.username
    group = request.args.get("group", "null")
    functype = request.args.get("functype", "null")

    try:
        ones = projectinfo.query.filter(projectinfo.business == group).order_by(projectinfo.project_name.desc()).all()
    except:
        return json.dumps({'project sql error':['error']})
    project = {}
    try:
        ones1 = userservicegroup.query.filter(userservicegroup.username == user, userservicegroup.servicegroup == group ).all()
        permissions = ones1[-1].permissions
    except:
        permissions = 'null'

    for x in ones:
        if user not in adminuser and x.environment == 'online':
            if functype == 'online':
                if permissions != 'online':
                    continue
            elif functype == 'project_admin':
                if permissions != 'online' and permissions != 'config':
                    continue
        if x.environment in project:
            project[x.environment].append(x.project_name)
        else:
            project[x.environment] = [x.project_name]

    return json.dumps(project)



@main.route("/pagelist", methods=["GET", "POST"])
@login_required
def pagelist():
    user = current_user.username
    if user in adminuser:
        pagelist = adminpagelist
    else:
        pagelist = userpagelist
    return json.dumps(pagelist)



@main.route("/rmpkl", methods=["GET", "POST"])
@login_required
def rmpkl():
    project = request.args.get("project","null")
    DIR = getdir(project)
    pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)
    try:
        os.remove(pklFile)
    except:
        pass
    return json.dumps(['ok'])


@main.route("/killtask", methods=["GET", "POST"])
@login_required
def killtask():
    R = {'status':'ok', 'log':'', 'data':''}
    project = request.args.get("project","null")
    if project == "null":
       return json.dumps(['project null'])
    DIR = getdir(project)
    shell_cmd = '''ps -eaf |grep deploy.py|grep -v grep |grep %s |awk '{print $2}' |xargs -i -t kill -9 {} ''' % (project)
    Result = shellcmd(shell_cmd)
    R['log'] = Result['log']
    R['status'] = Result['status']
    pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)
    try:
        os.remove(pklFile)
    except:
        pass
    return json.dumps(R)


@main.route("/clean_git_cache", methods=["GET", "POST"])
@login_required
def clean_git_cache():
    project = request.args.get("project","null")
    if project == "null":
        return json.dumps(['project null'])
    DIR = getdir(project)
    project_git_path = '%s/%s' %(DIR['git'], project)
    status = os.popen('mv -i  %s  %s.%s.clean' %(project_git_path, project_git_path,
                                                 time.strftime('%Y%m%d_%H%M'))   ).read()
    logging.info(status)

    return json.dumps([status])

@main.route("/add_group", methods=["GET", "POST"])
@login_required
def add_group():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        addgroupname = request.form.get("addgroupname","null").strip().split(' ')[0]
        if addgroupname == '' or addgroupname == 'null':
            raise Exception('ERROR: add groupname null')
        u = servicegroup(servicegroup=addgroupname)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/del_group", methods=["POST"])
@login_required
def del_group():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        groupname = request.form.get('selectgroup', 'null')
        if groupname == 'null':
            raise Exception('ERROR: servicegroup null')
        servicegroup.query.filter(servicegroup.servicegroup == groupname).delete()
        userservicegroup.query.filter(userservicegroup.servicegroup == groupname).delete()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/adduserservicegroup", methods=["GET", "POST"])
@login_required
def adduserservicegroup():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        username = request.form.get("username","null").strip().split(' ')[0]
        servicegroup = request.form.get("servicegroup","null").strip().split(' ')[0]
        permissions = request.form.get("permissions","null").strip().split(' ')[0]
        user = current_user.username
        if user not in adminuser or username == '' or username == 'null' or servicegroup == '' or servicegroup == 'null':
            raise Exception('ERROR: The current user has no rights')
        u = userservicegroup(username=username, servicegroup=servicegroup, permissions=permissions)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/deleteuserservicegroup", methods=["POST"])
@login_required
def deleteuserservicegroup():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = request.form.get('user', 'null')
        servicegroup = request.form.get('servicegroup', 'null')
        if user == "null" or servicegroup == 'null':
            raise Exception('ERROR: user or servicegroup null')
        userservicegroup.query.filter(userservicegroup.username == user, userservicegroup.servicegroup == servicegroup).delete()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/group_list", methods=["GET", "POST"])
@login_required
def group_list():
    user = request.args.get("user", "null")
    if user == "null":
        user = current_user.username

    try:
        if user in adminuser:
            ones = userservicegroup.query.all()
        else:
            ones = userservicegroup.query.filter(userservicegroup.username == user ).all()
    except:
        return json.dumps(['sql error'])
    grouplist = []
    for i in ones:
        if i.servicegroup != 'null':
            grouplist.append(i.servicegroup)
    grouplist = sorted(list(set(grouplist)))
    return json.dumps(grouplist)

@main.route("/group_list_all", methods=["GET", "POST"])
@login_required
def group_list_all():
    user = current_user.username
    if user in adminuser:
        try:
            ones = servicegroup.query.all()
        except:
            return json.dumps(['sql error or no authority'])

    grouplist = []
    for i in ones:
        if i.servicegroup != 'null':
            grouplist.append(i.servicegroup)
    grouplist = sorted(list(set(grouplist)))
    return json.dumps(grouplist)


@main.route("/group_list_user", methods=["GET", "POST"])
def group_list_user():
    user = request.args.get("user")
    try:
        if user in adminuser:
            ones = userservicegroup.query.all()
        else:
            ones = userservicegroup.query.filter(userservicegroup.username == user ).all()
    except:
        return json.dumps(['sql error'])
    grouplist = []
    for i in ones:
        if i.servicegroup != 'null':
            grouplist.append(i.servicegroup)
    grouplist = list(set(grouplist))
    return json.dumps(grouplist)


@main.route("/userservicegrouplist", methods=["GET", "POST"])
@login_required
def userservicegrouplist():
    user = request.args.get("user")
    try:
        ones = userservicegroup.query.filter(userservicegroup.username == user ).all()
    except:
        return json.dumps([['sql','error']])
    grouplist = []
    for i in ones:
        grouplist.append([i.servicegroup, i.permissions])
    return json.dumps(grouplist)



@main.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        adduser = request.form.get('adduser', 'null').strip().split(' ')[0]
        password = request.form.get('password', 'null').strip().split(' ')[0]
        user = current_user.username
        if adduser == 'null' or adduser == '' or password == 'null' or password == '':
            raise Exception('ERROR: user or password null')
        if user not in adminuser:
            raise Exception('ERROR: The current user has no rights')
        u = User(email='%s@cedar.cn' %adduser, username='%s' %adduser, password=password)
        User.query.filter(User.username == adduser).delete()
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/delete_user", methods=["GET", "POST"])
@login_required
def delete_user():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        deleteuser = request.form.get("deleteuser","null").strip().split(' ')[0]
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: The current user has no rights')
        User.query.filter(User.username == deleteuser).delete()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/user_list", methods=["GET", "POST"])
@login_required
def user_list():
    try:
        user = current_user.username
        if user in adminuser:
            userlist = []
            ones = User.query.all()
            for i in ones:
                userlist.append(i.username)
        else:
            return json.dumps(['ERROR: The current user has no rights'])

        return json.dumps(userlist)
    except:
        return json.dumps(['sql error'])


@main.route("/hostlist", methods=["GET", "POST"])
def hostlist():
    project = request.args.get("project","null")
    if project == "null":
        return json.dumps([['project null','error','null','null']])
    try:
        ones = projectinfo.query.filter(projectinfo.project_name == project ).all()
        Type = ones[0].type
        group = ones[0].business
        env = ones[0].environment

        ones1 = serverinfo.query.filter(serverinfo.project_name == project ).order_by(serverinfo.hostname).all()
    except:
        return json.dumps([['sql','error','null','null']])
    rl = []
    for i in ones1:
        rl.append([i.ip, i.hostname, i.project_name, Type, i.pnum, i.env, i.checkstatus, i.checktime, i.commitid, i.updatestatus, i.updatetime ]) 
    return json.dumps(rl)


@main.route("/hostlistall", methods=["GET", "POST"])
def hostlistall():
    try:
        ones = serverinfo.query.all()
        rl = []
        for i in ones:
            rl.append([i.ip, i.hostname, i.project_name])
        return json.dumps(rl)
    except:
        return json.dumps([['sql','error','null','null']])

@main.route("/iplistall", methods=["GET", "POST"])
def iplistall():
    try:
        ones = serverinfo.query.all()
        ipl = []
        for i in ones:
            ipl.append(i.ip)

        return json.dumps(list(set(ipl)))
    except:
        return json.dumps(['sqlerror'])


@main.route("/hostlisterr", methods=["GET", "POST"])
def hostlisterr():
    try:
        ones = serverinfo.query.filter(  serverinfo.checkstatus != 'RUNNING', 
                                         serverinfo.checkstatus != 'SSHOK',
                                         serverinfo.checkstatus != 'null'
                                      ).order_by(serverinfo.project_name).all()
    except:
        return json.dumps([['sql','error','null','null']])
    rl = []
    Type = 'null'

    for i in ones:
        rl.append([i.ip, i.hostname, i.project_name, Type, i.pnum, i.checkstatus, i.checktime, 
                   i.commitid, i.updatestatus, i.updatetime])
    return json.dumps(rl)

@main.route("/port_list", methods=["GET", "POST"])
@login_required
def port_list():
    try:
        ones = projectinfo.query.order_by(projectinfo.port).all()
    except Exception as err:
        return json.dumps([['sql','error','null','null']])
    portlist = []
    for i in ones:
        portlist.append([ i.port, i.project_name ])
    return json.dumps(portlist)

@main.route("/project_list", methods=["GET", "POST"])
@login_required
def project_list():
    try:
        ones = projectinfo.query.order_by(projectinfo.business).all()
    except Exception as err:
        return json.dumps([['sql','error','null','null']])
    projectlist = []
    for i in ones:
        projectlist.append([i.business, i.project_name, i.port  ])
    return json.dumps(projectlist)

@main.route("/project_info", methods=["GET", "POST"])
@login_required
def project_info():
    project = request.args.get("project", "null")
    if project == "null":
        return json.dumps(['business', 'environment', 'project null', 'type', 'port', 'git', 'branch'])
    try:
        ones = projectinfo.query.filter(projectinfo.project_name == project).first()
    except:
        return json.dumps(['business', 'environment', 'sql error', 'type', 'port', 'git', 'branch'])
    rl = [ ones.business, ones.environment,  ones.project, ones.type, ones.port, ones.git, ones.branch]
    return json.dumps(rl)
        


@main.route("/projectinfoall", methods=["GET", "POST"])
def projectinfoall():
    try:
        ones = projectinfo.query.all()
    except:
        return json.dumps( {'environment_project null':['git', 'branch', 'type', 'port', 'business']})
    rl = {}
    for i in ones:
        rl['%s_%s' %(i.environment, i.project)] = [i.git, i.branch, i.type, i.port, i.business]
    return json.dumps(rl)



@main.route("/config_info", methods=["GET", "POST"])
@login_required
def config_info():
    project_name = request.args.get("project", "null")
    if project_name == "null":
        return json.dumps({'project null':'config'})
    try:
        ones = project_config.query.filter(project_config.project_name == project_name).first()
    except:
        return json.dumps({'sql error':'config'})

    rl = [  ['make',         ones.make],
            ['supervisor',   ones.supervisor],
            ['config',       ones.config],
            ['remarks',      ones.remarks],
            ['startcmd',     ones.startcmd],
            ['packfile',     ones.packfile], 
            ['istag',        ones.istag],
            ['checkport',    ones.checkport],
            ['checkhttp',    ones.checkhttp],
            ['httpurl',      ones.httpurl],
            ['httpcode',     ones.httpcode]
         ]
    return json.dumps(rl)


@main.route("/add_project", methods=["POST"])
@login_required
def add_project():
    R = {'status':'ok', 'log':'', 'data':''}

    try:
        business = request.form.get('business', "null").strip()
        environment = request.form.get('environment', "null").strip()
        project = request.form.get('project', "null").strip().lower()
        program_type = request.form.get('type', "null").strip()
        port = str(request.form.get('port', "0")).strip()
        git = request.form.get('git', "null").strip()
        branch = request.form.get('branch', "null").strip()
        if not port:
            port = '0'
        if not port.isdigit():
            return json.dumps({'status':'parameter error. port Not a Number %s %s' %(port, type(port))})
    
        if project == "null" or environment == "null" or branch == "null" or program_type == "null" or git == "null":
            raise Exception('ERROR: parameter error')
    
        project_name = environment + '_' + project
    
        ones = projectinfo.query.filter(projectinfo.project_name == project_name ).first()
        if ones != None:
            raise Exception('ERROR: project already exists')
        newproject = projectinfo(  project_name = project_name, 
                                   business     = business, 
                                   environment  = environment, 
                                   project      = project, 
                                   type         = program_type, 
                                   port         = port, 
                                   git          = git, 
                                   branch       = branch
                                )
        db.session.add(newproject)
        db.session.commit()
    
        if program_type == 'python':
            supervisor = supervisor_python_conf
        if program_type == 'nodejs':
            supervisor = supervisor_nodejs_conf
        elif program_type == 'go' or program_type == 'golang':
            supervisor = supervisor_go_conf
        elif program_type == 'sh':
            supervisor = supervisor_sh_conf
        elif program_type == 'java':
            supervisor = catalina_sh
            config = server_xml
    
        configadd = project_config(  project_name = project_name, 
                                     make         = '',
                                     supervisor   = supervisor,
                                     config       = '',
                                     remarks      = 'remarks',
                                     startcmd     = '',
                                     packfile     = '',
                                     istag        = 'no',
                                     checkport    = 'no',
                                     checkhttp    = 'no',
                                     httpurl      = '/',
                                     httpcode     = '200')
        db.session.add(configadd)
        db.session.commit()

    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/add_host", methods=["POST"])
@login_required
def add_host():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project      = request.form.get('project',      "null").strip()
        hostname     = request.form.get('hostname',     "null").strip()
        host         = request.form.get('host',         "null").strip()
        pnum         = request.form.get('pnum',         "1"   ).strip()
        env          = request.form.get('env',          ""    ).strip()
        if pnum == '':
            pnum = '1'
        if project == "null" or host == "null" or project == "" or host == "":
            raise Exception('ERROR: parameter error')

        if hostname == '' or hostname == 'null':
            Result = getHostname(host)
            if Result['status'] == 'ok':
                hostname = Result['log'].strip().split('.')[0]
            else:
                raise Exception('ERROR: get hostname error')
    
        ones1 = serverinfo.query.filter(serverinfo.project_name == project, serverinfo.ip == host).all()
        if len(ones1) != 0:
            raise Exception('ERROR: host exist.')
    
        ones = projectinfo.query.filter(projectinfo.project_name == project ).first()
        if int(ones.port) >3000:
            t = set(range(int(ones.port), int(ones.port) + int(pnum)))
            ones3 = serverinfo.query.filter(serverinfo.ip == host).all()
            for ones3line in ones3:
                ones4 = projectinfo.query.filter(projectinfo.project_name == ones3line.project_name ).first()
                s = set(range(int(ones4.port), int(ones4.port) + int(ones3line.pnum) ))
                repeatport = s.intersection(t)
                if repeatport:
                    raise Exception('ERROR: host port %s %s exist conflict.' %(host, str(list(repeatport)) ) )
    
        newserver = serverinfo(project, hostname, host, pnum, env, 'checkstatus', 'checktime', 'commitid', 'updatestatus', 'updatetime')
        db.session.add(newserver)
        db.session.commit()
        ones1 = serverinfo.query.filter(serverinfo.project_name == project, serverinfo.ip == host).first()
        ones2 = project_config.query.filter(project_config.project_name == project ).first()

        hir = hostInit(project, host, ones.type)
        if hir != 'ok':
            raise Exception(hir)
    
        dcr = deployConfig(project, host, ones, ones1, ones2)
        if dcr != 'ok':
            raise Exception(dcr)
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/del_host", methods=["POST"])
@login_required
def del_host():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project = request.form.get('project', 'null')
        host = request.form.get('host', 'null')
        if project == 'null' or host == 'null':
            raise Exception('ERROR: host null')
        currentuser = current_user.username
        if currentuser not in adminuser and project.startswith('online_'):
            raise Exception('ERROR: No authority')
        logging.warning('del_host: %s, %s, %s' %(currentuser, project, host) )
        serverinfo.query.filter(serverinfo.project_name == project, serverinfo.ip == host).delete()
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "mv %s/%s.conf  %s/%s.conf.%s.bak; supervisorctl reread;supervisorctl update" ''' %( 
                           exec_user, host, supervisor_conf_dir, project, supervisor_conf_dir, project, time.strftime('%Y%m%d_%H%M%S'))
        Result = shellcmd(shell_cmd)
        if Result['status'] != 'ok':
            raise Exception(Result['log'])
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/update_host", methods=["POST"])
@login_required
def update_host():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project      = request.form.get('project',     'null').strip()
        hostname     = request.form.get('hostname',    'null').strip()
        ip           = request.form.get('hostip',      'null').strip()
        pnum         = request.form.get('pnum',        '1'   ).strip()
        env          = request.form.get('env',         ''    ).strip()
        checkstatus  = request.form.get('checkstatus', 'null').strip()
        checktime    = request.form.get('checktime',   'null').strip()
        commitid     = request.form.get('commitid',    'null').strip()
        updatestatus = request.form.get('updatestatus','null').strip()
        updatetime   = request.form.get('updatetime',  'null').strip()
    
        if project == 'null' or ip == 'null':
            raise Exception('ERROR: host null')
        currentuser = current_user.username
        logging.warning('update_host: %s, %s, %s' %(currentuser, project, ip) )
        serverinfo.query.filter(  serverinfo.project_name == project, 
                                  serverinfo.ip == ip
                               ).update({
                                  "hostname" : hostname, 
                                  "pnum"     : pnum, 
                                  "env"      : env
                               })
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/deploy_config", methods=["POST"])
@login_required
def deploy_config():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project = request.form.get('project', 'null')
        host = request.form.get('host', 'null')
        if project == 'null' or host == 'null':
            raise Exception('ERROR: host null')

        ones = projectinfo.query.filter(projectinfo.project_name == project ).first()
        ones1 = serverinfo.query.filter(serverinfo.project_name == project, serverinfo.ip == host).first()
        ones2 = project_config.query.filter(project_config.project_name == project ).first()

        dcr = deployConfig(project, host, ones, ones1, ones2)
        if dcr != 'ok':
            raise Exception(dcr)
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/deploy", methods=["POST"])
@login_required
def deploy():
    taskid = str(time.time())
    currentuser = current_user.username
    operating_time = time.strftime('%Y%m%d_%H%M%S')

    project = request.form.get("project","null")
    host = request.form.get("client","null")
    operation = request.form.get("operation","null")

    DIR = getdir(project)

    if operation == 'serviceUpdate':
        tag = '%s-%s' %(project.split('_')[0], time.strftime('%Y%m%d_%H-%M-%S',time.localtime( int(float(taskid)) ) ) )
    elif operation == 'serviceFallback' or operation == 'serviceFastback':
        tag = request.form.get("tag","null")
    else:
        tag = "null"

    pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)

    R = {"output":"","taskid":taskid,"operation":operation,"hostlist":host,"project":project,"tag":tag,"status":"wait"}

    try:
        if host == "null" and project == "null" and operation == "null":
            raise Exception('ERROR: project or host or operation null')
        if os.path.isfile(pklFile):
            raise Exception('WARNING: Repeat the update, Please wait')
        ones = projectinfo.query.filter(projectinfo.project_name == project ).all()
        Type = ones[0].type
        group = ones[0].business
        env = ones[0].environment
        if currentuser not in adminuser:
            ones1 = userservicegroup.query.filter(  userservicegroup.username == currentuser, 
                                                    userservicegroup.servicegroup == group 
                                                 ).all()
            permissions = ones1[-1].permissions
            if env == "online" and permissions != 'online':
                raise Exception('ERROR: user not online deploy permissions')
            if operation == 'serviceUpdate' and env == "online" and group not in unlimit and project not in unlimitProject and not check_time():
                raise Exception('ERROR: online deploy time: Working day  10:00-11:30.  14:00-17:30.  19:00-20:00')
        online_update_file = open(pklFile, 'wb')
        cPickle.dump('%s %s %s' %(currentuser, operation, operating_time),online_update_file)
        online_update_file.close()
        s = os.system(   '''(cd %s/app/main/;nohup python deploy.py "%s" "%s" "%s" "%s" "%s" "%s" "%s") >>%s/%s.log 2>&1    &'''  
                         %(sys.path[0], project, tag, taskid, host, operation, currentuser, 'reason', DIR['log'], project) )
        R['output'] = 'INFO: Please wait. %s in progress' %(operation)
        logPath = '%s/%s.log' %(DIR['result'], tag)
        newupdateoperation = updateoperation(taskid,  project, host, tag, operating_time, operation, currentuser, R['status'], 'commitid', 0, logPath)
        db.session.add(newupdateoperation)
        db.session.commit()
    except Exception as err:
        R['output'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)
    


@main.route("/cmdreturns", methods=["GET", "POST"])
@login_required
def cmdreturns():
    taskid = request.args.get('taskid', 'null')
    if taskid == "null":
        return json.dumps([['taskid','null']])
    try:
        ones = updateoperation.query.filter(updateoperation.taskid == taskid ).all()
        project  = ones[0].project_name
        status   = ones[0].status
        progress = ones[0].progress
        logpath  = ones[0].logpath
        logfile  = file(logpath,'r')
        result   = logHandle(logfile.read())
        logfile.close()
    except:
        return json.dumps([['sql','error']])
    rl = {'taskid': taskid, 'status': status, 'project': project, 'progress': progress, 'result': result }
    logging.info(str(rl))
    return json.dumps(rl)



@main.route("/online_log_time", methods=["GET", "POST"])
@login_required
def online_log_time():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps([['null', 'null', 'null', 'null', 'ERROR: project null']])
    try:
        ones = updateoperation.query.filter(  updateoperation.project_name == project
                                           ).order_by(updateoperation.taskid.desc()).limit(200)
    except:
        return json.dumps([['null', 'null', 'null', 'null', 'ERROR: SQL not correct']])
    rl = []
    for i in ones:
        rl.append([i.operation, i.taskid, i.tag, i.project_name, i.status, i.user, i.commitid])
    return json.dumps(rl)


@main.route("/online_log_all", methods=["GET", "POST"])
@login_required
def online_log_all():
    try:
        ones = updateoperation.query.filter(  updateoperation.project_name.like('online_%'), 
                                              updateoperation.taskid>int(time.time())-604800, 
                                              updateoperation.operation.in_ ([ 'serviceUpdate','serviceFastback','serviceFallback','serviceRestart','serviceExpansion','serviceFastrestart']) 
                                           ).order_by(updateoperation.taskid.desc()).all()
    except:
        return json.dumps([['null', 'null', 'null', 'null', 'ERROR: SQL not correct']])
    rl = []
    for i in ones:
        rl.append([i.operation, i.taskid, i.tag, i.project_name, i.status, i.user, i.commitid])
    return json.dumps(rl)


@main.route("/online_tag", methods=["GET", "POST"])
@login_required
def online_tag():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps(['ERROR: project null'])

    try:
        ones = updateoperation.query.filter(  updateoperation.project_name == project, 
                                              updateoperation.operation.in_ ([ 'serviceUpdate']),
                                              updateoperation.status == 'ok'
                                           ).order_by(updateoperation.taskid.desc()).limit(15)
    except:
        return json.dumps(['ERROR: SQL not correct'])
    rl = []
    for i in ones:
        rl.append(i.tag)
    return json.dumps( sorted(list(set(rl)), reverse=True))


@main.route("/current_tag", methods=["GET", "POST"])
def current_tag():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps(['ERROR: project null'])
    try:
        ones = updateoperation.query.filter(  updateoperation.project_name == project, 
                                              updateoperation.operation.in_ ([ 'serviceUpdate','serviceFallback','serviceFastback']), 
                                              updateoperation.status == 'ok' 
                                           ).order_by(updateoperation.taskid.desc()).limit(2)
        rl = [ones[0].tag]
    except:
        return json.dumps(['null update'])
    logging.info('tag: %s' %rl[0])
    return json.dumps(rl)



@main.route("/lastlog", methods=["GET", "POST"])
@login_required
def lastlog():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps([['project','null']])
    try:
        ones = updateoperation.query.filter( updateoperation.project_name == project, 
                                             updateoperation.status != 'wait',
                                           ).order_by(updateoperation.taskid.desc()).limit(1)
        taskid   = ones[0].taskid
        project  = ones[0].project_name
        status   = ones[0].status
        progress = ones[0].progress
        logpath  = ones[0].logpath
        logfile  = file(logpath,'r')
        result   = logHandle(logfile.read())
        logfile.close()
    except:
        return json.dumps([['sql','error']])
    rl = {'taskid': taskid, 'status': status, 'project': project, 'progress': progress, 'result': result }
    return json.dumps(rl)



@main.route("/update_project", methods=["POST"])
@login_required
def update_project():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        business = request.form.get('business', "null").strip()
        environment = request.form.get('environment', "null").strip()
        project = request.form.get('project', "null").strip()
        program_type = request.form.get('type', "null").strip()
        port = request.form.get('port', "0").strip()
        git = request.form.get('git', "null").strip()
        branch = request.form.get('branch', "null").strip()
        if project == "null" or environment == "null" or branch == "null" or program_type == "null" or git == "null":
            raise Exception('ERROR: parameter error')
        project_name = environment + '_' + project

        currentuser = current_user.username
        if currentuser not in adminuser and environment == 'online':
            raise Exception('ERROR: update_project no authority')

        logging.warning('update_project: %s, %s, %s, %s, %s, %s, %s' %(
                currentuser, business, program_type, project_name, git, branch, port) )
    
        projectinfo.query.filter(projectinfo.project_name == project_name).update({
                             "business"    : business, 
                             "environment" : environment, 
                             "project"     : project, 
                             "type"        : program_type, 
                             "port"        : port, 
                             "git"         : git, 
                             "branch"      : branch
                             })

        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/update_config", methods=["POST"])
@login_required
def update_config():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project_name = request.form.get('project',    "null").strip()
        make         = request.form.get('make',       "null").strip()
        supervisor   = request.form.get('supervisor', "null").strip()
        config       = request.form.get('config',     "null").strip()
        remarks      = request.form.get('remarks',    "null").strip()
        startcmd     = request.form.get('startcmd',   "null").strip()
        packfile     = request.form.get('packfile',   "null").strip()
        istag        = request.form.get('istag',      "null").strip()
        checkport    = request.form.get('checkport',  "null").strip()
        checkhttp    = request.form.get('checkhttp',  "null").strip()
        httpurl      = request.form.get('httpurl',    "null").strip()
        httpcode     = request.form.get('httpcode',   "null").strip()
        if project_name == "null":
            raise Exception('ERROR: project error')
        currentuser = current_user.username
        logging.warning('update_config: %s, %s' %(currentuser, project_name) )
        project_config.query.filter(project_config.project_name == project_name).update({
                "make"        : make, 
                "supervisor"  : supervisor, 
                "config"      : config, 
                "remarks"     : remarks, 
                "startcmd"    : startcmd, 
                "packfile"    : packfile, 
                "istag"       : istag, 
                "checkport"   : checkport, 
                "checkhttp"   : checkhttp, 
                "httpurl"     : httpurl, 
                "httpcode"    : httpcode })

        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/online_statistics", methods=["GET", "POST"])
@login_required
def online_statistics():
    try:
        monday=datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        monday_timestamp=time.mktime(time.strptime(monday.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))

        online_total=updateoperation.query.filter(updateoperation.project_name.like('online_%'),updateoperation.status.notlike('error'),updateoperation.taskid<monday_timestamp, updateoperation.taskid>monday_timestamp-2419200).all()

        statistical_result = {}

        for i in online_total:
            if i.project_name not in statistical_result:
                statistical_result[i.project_name] = [0,0,0,0,0,0,0,0,0,0,0,0]

            timestamp = int( float(i.taskid) )
            if timestamp < monday_timestamp and timestamp > monday_timestamp-604800:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project_name][0] = statistical_result[i.project_name][0] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project_name][1] = statistical_result[i.project_name][1] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project_name][2] = statistical_result[i.project_name][2] + 1
            elif timestamp < monday_timestamp and timestamp > monday_timestamp-1209600:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project_name][3] = statistical_result[i.project_name][3] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project_name][4] = statistical_result[i.project_name][4] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project_name][5] = statistical_result[i.project_name][5] + 1
            elif timestamp < monday_timestamp and timestamp > monday_timestamp-1814400:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project_name][6] = statistical_result[i.project_name][6] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project_name][7] = statistical_result[i.project_name][7] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project_name][8] = statistical_result[i.project_name][8] + 1
            elif timestamp < monday_timestamp and timestamp > monday_timestamp-2419200:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project_name][9] = statistical_result[i.project_name][9] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project_name][10] = statistical_result[i.project_name][10] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project_name][11] = statistical_result[i.project_name][11] + 1
        return json.dumps(statistical_result)
    except:
        return json.dumps({'status':["sql error"]})



@main.route("/lock_check", methods=["GET", "POST"])
def lock_check():
    R = {'status':'ok', 'log':'', 'data':'', 'user':''}
    try:
        project = request.args.get('project', "null")
        DIR = getdir(project)
        pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)
    
        if os.path.isfile(pklFile):
            lock_file = open(pklFile,'rb')
            lock_user = cPickle.load(lock_file)
            lock_file.close()
            R['user'] = lock_user
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)
    

@main.route("/add_workorder", methods=["POST"])
@login_required
def add_workorder():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        group = str(request.form.get('group', 'null')).strip()
        project = str(request.form.get('project', 'null')).strip()
        remarks = str(request.form.get('remarks', 'null')).strip()
    
        if project == 'null':
            raise Exception('ERROR: project null')
    
        user = current_user.username
        applicationtime = str(time.time())
        status = 'wait'
        executor = ''
        completiontime = ''
    
        newworkorder = workorder( group, project, user, applicationtime, status, executor, completiontime, remarks)
        db.session.add(newworkorder)
        db.session.commit()
    
        data = {
                "msgtype": "text",
                "text": {
                    "content": "%s\n%s 提交工单" %(project, user)
                }
            }
    
        headers = {'content-type': 'application/json'}
        r = requests.post(url=sreRobot, data=json.dumps(data), headers=headers, timeout=2).json()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/update_workorder", methods=["POST"])
@login_required
def update_workorder():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        applicationtime = str(request.form.get('applicationtime', 'null')).strip()
        if project == 'null':
            raise Exception('ERROR: project null')
        oldworkorder = workorder.query.filter(workorder.applicationtime == applicationtime).one()
        oldworkorder.status = 'done'
        oldworkorder.executor = current_user.username
        oldworkorder.completiontime = str(time.time())
        db.session.flush()
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)




@main.route("/wait_workorder", methods=["GET", "POST"])
@login_required
def wait_workorder():
    user = current_user.username
    try:
        if user in adminuser:
            ones = workorder.query.filter(workorder.status == 'wait' ).all()
        else:
            ones = workorder.query.filter(workorder.status == 'wait', workorder.applicant == user ).all()
    except Exception as err:
        logging.error(str(err))
        return json.dumps([['status','select workorder sql error!!!']])

    workorderlist = []
    for i in ones:
        workorderlist.append([i.group, i.project, i.applicant, i.applicationtime, i.status, i.executor, i.completiontime, i.remarks])

    return json.dumps(workorderlist)


@main.route("/done_workorder", methods=["GET", "POST"])
@login_required
def done_workorder():

    user = current_user.username

    try:
        if user in adminuser:
            ones = workorder.query.filter(workorder.status == 'done' ).order_by(workorder.applicationtime.desc()).limit(200)
        else:
            ones = workorder.query.filter(workorder.status == 'done', workorder.applicant == user ).order_by(workorder.applicationtime.desc()).limit(100)
    except Exception as err:
        logging.error(str(err))
        return json.dumps([['status','select workorder sql error!!!']])

    workorderlist = []
    for i in ones:
        workorderlist.append([i.group, i.project, i.applicant, i.applicationtime, i.status, i.executor, i.completiontime, i.remarks])

    return json.dumps(workorderlist)


@main.route("/expansion", methods=["POST"])
def expansion():

    taskid = str(time.time())
    project = request.form.get('project', 'null')
    host = request.form.get('host', 'null')
    hostname = request.form.get('hostname', 'null')
    reason = request.form.get('reason', 'null')
    currentuser = 'expansion'
    operation = 'serviceExpansion'
    tag = 'null'
    rtime = time.strftime('%Y%m%d_%H%M%S')

    expansionInfo = 'expansion: %s %s %s %s' %(project, host, hostname, reason)

    logging.info(expansionInfo)

    R = {"status":"ok","output":expansionInfo,"taskid":taskid,"operation":operation,"host":host,"project":project,"tag":tag}

    try:
        if project == "null" or host == "null" or host == "ecsIpFail":
            raise Exception('ERROR: expansion parameter null. %s' %expansionInfo)
        shell_cmd = '''ssh -o StrictHostKeyChecking=no  -o ConnectTimeout=2 %s@%s "echo test" ''' %(exec_user, host)
        i=0
        while i<5:
            Result = shellcmd(shell_cmd)
            status = Result['status']
            logging.info(Result['log'])
            logging.info('expansion ssh retry: %d' %i)
            if status == 'ok':
                break
            else:
                i=i+1
                time.sleep(5)
        if status != 'ok':
            raise Exception('ERROR: expansion host %s ssh fail. %s' %(host, expansionInfo))

        DIR = getdir(project)

        pnum = "1"
        newserver = serverinfo(project, hostname, host, pnum, 'checkstatus', 'checktime', 'commitid', 'updatestatus', 'updatetime')
        db.session.add(newserver)
        db.session.commit()
        ones = projectinfo.query.filter(projectinfo.project_name == project ).first()
        ones1 = serverinfo.query.filter(serverinfo.project_name == project, serverinfo.ip == host).first()
        ones2 = project_config.query.filter(project_config.project_name == project ).first()
        hir = hostInit(project, host, ones.type)
        if hir != 'ok':
            raise Exception('ERROR: expansion host init error.  %s %s' % (expansionInfo, hir ))
        dcr = deployConfig(project, host, ones, ones1, ones2)
        if dcr != 'ok':
            raise Exception('ERROR: expansion deploy config error.  %s %s' % (expansionInfo, dcr ))
        s = os.system(   '''(nohup python %s/app/main/deploy.py "%s" "%s" "%s" "%s" "%s" "%s" "%s") >>%s/%s.log 2>&1    &'''
                        %(sys.path[0], project, tag, taskid, host, operation, currentuser, reason, DIR['log'], project) )
    except Exception as err:
        R['output'] = str(err)
        R['status'] = 'fail'
        headers = {'Content-Type':'application/json'}
        content = "%s\n%s: %s %s\nHost: %s\nReason: %s" %(rtime, project, operation, R['status'], host, reason)

        ExpansionHost = {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
        try:
            requests.post(url=sreRobot, headers=headers, data=json.dumps(ExpansionHost))
        except Exception as err:
            logging.error(str(err))
    try:
        logPath = '%s/%s.log' %(DIR['result'], project)
        newupdateoperation = updateoperation(taskid, project, host, tag, rtime, operation, currentuser, R['status'], 'commitid', 0, logPath)
        db.session.add(newupdateoperation)
        db.session.commit()
    except Exception as err:
        logging.error(str(err))
    return json.dumps(R)


@main.route("/reduced", methods=["POST"])
def reduced():
    try:
        project = request.form.get('project', "null")
        host = request.form.get('host', "null")
        reason = request.form.get('reason', "null")
        operation = 'scaleDown'
        R = {'status':'ok', 'log':'', 'data':'', 'project':project, 'host':host}
        if project == "null" or host == "null":
            raise Exception('ERROR: project or host null')
        logging.info('INFO: %s %s reduced' %(project, host))
        serverinfo.query.filter(serverinfo.project_name == project, serverinfo.ip == host).delete()
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "mv %s/%s.conf  %s/%s.conf.%s.bak; supervisorctl reread;supervisorctl update"  ''' %( 
                           exec_user, host, supervisor_conf_dir, project, supervisor_conf_dir, project, time.strftime('%Y%m%d_%H%M%S'))
        Result = shellcmd(shell_cmd)
        if Result['status'] != 'ok':
            raise Exception('ERROR: %s %s delete supervisor conf fail. %s' %(project, host, Result['log']))
        headers = {'Content-Type':'application/json'}
        endtime = time.strftime('%Y-%m-%d %H:%M:%S')
        content = "%s\n%s: %s %s\nHost: %s\nReason: %s" %(endtime, project, operation, R['status'], host, reason)
        ExpansionHost = {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
        requests.post(url=sreRobot, headers=headers, data=json.dumps(ExpansionHost))
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/get_area", methods=["GET", "POST"])
def get_area():
    bigbusiness = request.args.get("bigbusiness", "null")
    if bigbusiness == 'pp-online':
        area={'shal-d':'阿里云上海-D区','shal-f':'阿里云上海-F区','shal-e':'阿里云上海-E区','bjaws-d':'aws北京-D区'}
    elif bigbusiness == 'pp-test':
        area={'shal-d':'阿里云上海-D区'}
    elif bigbusiness == 'zy-online':
        area={'shal-d':'阿里云上海-D区','shal-f':'阿里云上海-F区','bjal-d':'阿里云北京-D区'}
    elif bigbusiness == 'zy-test':
        area={'shal-d':'阿里云上海-D区','shal-f':'阿里云上海-F区'}
    elif bigbusiness == 'hanabi-online':
        area={'shal-f':'阿里云上海-F区'}
    elif bigbusiness == 'hanabi-test':
        area={'shal-d':'阿里云上海-D区'}
    else:
        area={'error':'无可用区'}
    return json.dumps(area)


@main.route("/get_configuration", methods=["GET", "POST"])
def get_configuration():
    area = request.args.get("area", "null")
    if area == 'shal-d':
        configuration={'shal-4c8g':'4c8g计算网络增强型','shal-4c8g':'4c8g高主频型','shal-8c16g':'8c16g计算网络增强型','shal-8c32g':'8c32g内存型',}
    elif area == 'shal-f':
        configuration={'shal-4c8g':'4c8g计算型','shal-8c16g':'8c16g计算型','shal-8c32g':'8c32g内存型',}
    elif area == 'shal-e':
        configuration={'shal-4c8g':'4c8g计算型'}
    elif area == 'bjaws-d':
        configuration={'bjaws-4c8g':'4c8g共享型','bjaws-8c16g':'8c16g'}
    else:
        configuration={'error':'无可用配置'}
    return json.dumps(configuration)


@main.route("/create_hosts", methods=["GET", "POST"])
@login_required
def create_hosts():
    bigbusiness = request.form.get("bigbusiness", "null")
    area = request.form.get("area", "null")
    configuration = request.form.get("configuration", "null")
    image = request.form.get("image", "null")
    hostnames = request.form.get("hostnames", "null")

    create_hosts_taskid = 'ceshi-id-xx'
    log = '%s\n%s\n%s\n%s\n%s' %(bigbusiness,area,configuration,image,hostnames)
    r = {'status':'ok','hostnames':hostnames,'create_hosts_taskid':create_hosts_taskid,'log':log}
    return json.dumps(r)

@main.route("/get_create_hosts_result", methods=["GET", "POST"])
@login_required
def get_create_hosts_result():
    taskid = request.args.get("taskid", "null")
    log = '执行完成\n初始化完成\nok'
    r = {'status':'ok','taskid':taskid,'log':log}
    return json.dumps(r)



