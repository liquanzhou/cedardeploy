#!/usr/bin/env python
# coding: utf-8
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
from app.config import *



def check_time():
    T = time.localtime(time.time())
    WeekT = [0,1,2,3,4]
    AllT = [10,14,15,16,19]
    HalfT = [11,17]

    if int(T[6]) in WeekT:
        if int(T[3]) in AllT:
            return True
        elif int(T[3]) in HalfT:
            if int(T[4]) < 31:
                return True
        return False

def shellcmd(shell_cmd):
    s = subprocess.Popen( shell_cmd , shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE  )
    loginfo, stderr = s.communicate()
    return_status = s.returncode
    if return_status == 0:
        status = 'ok'
    else:
        loginfo = loginfo + '\n' + stderr
        status = 'fail'
    return {'status':status,'log':loginfo}


def writefile(path, content):
    f = open(path, 'w')
    f.write(content)
    f.flush()
    f.close()


def getdir(project):
    DIR = {}
    dir_path_git    = path_git.rstrip('/') + '/'    + project
    dir_path_log    = path_log.rstrip('/') + '/'    + project
    dir_path_lock   = path_lock.rstrip('/') + '/'   + project
    dir_path_conf   = path_conf.rstrip('/') + '/'   + project
    dir_path_result = path_result.rstrip('/') + '/' + project

    shell_cmd = '''mkdir -p %s %s %s %s %s ''' %(dir_path_git, dir_path_log, dir_path_lock, dir_path_conf, dir_path_result)
    Result = shellcmd(shell_cmd)

    DIR['git']     = dir_path_git
    DIR['log']     = dir_path_log
    DIR['lock']    = dir_path_lock
    DIR['conf']    = dir_path_conf
    DIR['result']  = dir_path_result

    return DIR

def getHostname(host):
    shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "hostname" ''' %(exec_user, host)
    Result = shellcmd(shell_cmd)
    return Result


def hostInit(project, host, Type):
    if Type == 'java':
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "cp -a %s/tomcat8_install_template %s/%s " ''' %(
                       exec_user, host, remote_host_path, remote_host_path, project)
    else:
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "mkdir -p %s %s" ''' %(
                       exec_user, host, supervisor_log_path, remote_host_path)
    Result = shellcmd(shell_cmd)
    if Result['status'] != 'ok':
        return Result['log']
    else:
        return Result['status']


def deployConfig(project, host, ones, ones1, ones2):
    try:
        if ones.type in supervisord_list:
            DIR = getdir(project)

            supervisor_conf = ones2.supervisor

            variable = {
                '$USER$':                exec_user,
                '$HOST_PATH$':           remote_host_path,
                '$environment$':         ones.environment,
                '$project$':             ones.project,
                '$ip$':                  host,
                '$pnum$':                ones1.pnum,
                '$env$':                 ones1.env,
                '$port$':                str(ones.port),
                '$ajpport$':             str(int(ones.port)-105),
                '$shutdownport$':        str(int(ones.port)-75)
            }
            for n, v in variable.items():
                supervisor_conf = supervisor_conf.replace(n, v)
            supervisor_conf_path = '%s/%s_%s_supervisor.conf' %(DIR['conf'], project, host)
            remote_supervisor_conf_path = '%s@%s:%s/%s.conf' %(exec_user, host, supervisor_conf_dir, project)
            writefile(supervisor_conf_path, supervisor_conf)

            shell_cmd = '''scp -o StrictHostKeyChecking=no -o ConnectTimeout=2  %s  %s  > /dev/null  ''' %(
                           supervisor_conf_path, remote_supervisor_conf_path)
            Result = shellcmd(shell_cmd)
            if Result['status'] != 'ok':
                raise Exception(Result['log'])

            shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "supervisorctl reread" ''' %(
                           exec_user, host)
            Result = shellcmd(shell_cmd)
            if Result['status'] != 'ok':
                raise Exception(Result['log'])
        return 'ok'
    except Exception as err:
        return str(err)


def logHandle(logtext):
    result   = logtext.replace(
                    '<', '').replace(
                    '>', '').replace(
                    'ERROR:', '<span style="color: red">ERROR:</span>').replace(
                    'INFO:', '<span style="color: green">INFO:</span>').replace(
                    'WARN:', '<span style="color: yellow">WARN:</span>').replace(
                    'Git Code update:', '<span style="color: blue">Git Code update:</span>').replace(
                    'Code Compile:', '<span style="color: blue">Code Compile:</span>').replace(
                    'Version Backup:', '<span style="color: blue">Version Backup:</span>').replace(
                    'Update Config:', '<span style="color: blue">Update Config:</span>').replace(
                    'Del Service Start:', '<span style="color: blue">Del Service   Start:</span>').replace(
                    'Restart Service:', '<span style="color: blue">Restart Service:</span>').replace(
                    'Check Start:', '<span style="color: blue">Check Start:</span>').replace(
                    'Autotest Start:', '<span style="color: blue">Autotest Start:</span>').replace(
                    'Reg Service Start:', '<span style="color: blue">Reg Service   Start:</span>').replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;').replace(
                    '\n', '<br>'
                )

    return result

crontab_conf = '''#01 01 * * * $HOST_PATH$$environment$_$project$/deploy_start.sh >> $supervisor_log_path$/$environment$_$project$.log  2>&1 
'''


config_list = '''
#config list
'''


supervisor_python_conf = '''[program:$environment$_$project$]
environment=HOME=/home/$USER$,PROJECT_ENV="$environment$",PROJECT_NAME=$project$,PROJECT_PORT=$port$,PROJECT_PATH="$HOST_PATH$$environment$_$project$/",PRODUCT_ENV="",$env$
directory=$HOST_PATH$$environment$_$project$/
command=/usr/bin/python  $HOST_PATH$$environment$_$project$/main.py --port=%(process_num)02d
process_name=%(process_num)d
user=$USER$
startretries=5
stopsignal=TERM
autorestart=true
stopasgroup=true
redirect_stderr=true
stdout_logfile=$supervisor_log_path$/%(program_name)s-%(process_num)d.log
stdout_logfile_maxbytes=500MB
stdout_logfile_backups=10
loglevel=info
numprocs = $pnum$
numprocs_start=$port$
'''

supervisor_nodejs_conf = '''[program:$environment$_$project$]
environment=HOME=/home/$USER$,PROJECT_ENV="$environment$",PROJECT_NAME=$project$,PROJECT_PORT=$port$,PROJECT_PATH="$HOST_PATH$$environment$_$project$/",PRODUCT_ENV="",$env$
directory=$HOST_PATH$$environment$_$project$/
command=/usr/bin/node $HOST_PATH$$environment$_$project$/index.js --port=%(process_num)d
process_name=%(process_num)d
user=$USER$
startretries=5
stopsignal=TERM
autorestart=true
stopasgroup=true
redirect_stderr=true
stdout_logfile=$supervisor_log_path$/%(program_name)s-%(process_num)d.log
stdout_logfile_maxbytes=500MB
stdout_logfile_backups=10
loglevel=info
numprocs = $pnum$
numprocs_start=$port$
'''

supervisor_go_conf = '''[program:$environment$_$project$]
environment=HOME=/home/$USER$,PROJECT_ENV="$environment$",PROJECT_NAME=$project$,PROJECT_PORT=$port$,PROJECT_PATH="$HOST_PATH$$environment$_$project$/",PRODUCT_ENV="",$env$
directory=$HOST_PATH$$environment$_$project$/
command=$HOST_PATH$$environment$_$project$/bin/$project$ -f $HOST_PATH$$environment$_$project$/etc/$environment$_$project$.conf
process_name = %(process_num)d
user=$USER$
startretries=5
stopsignal=TERM
stopasgroup=true
autorestart=true
redirect_stderr=true
stdout_logfile=$supervisor_log_path$/%(program_name)s.log
stdout_logfile_maxbytes=500MB
stdout_logfile_backups=10
loglevel=info

'''

supervisor_sh_conf = '''[program:$environment$_$project$]
environment=HOME=/home/$USER$,PROJECT_ENV="$environment$",PROJECT_NAME=$project$,PROJECT_PORT=$port$,PROJECT_PATH="$HOST_PATH$$environment$_$project$/",PRODUCT_ENV="",$env$
directory=$HOST_PATH$$environment$_$project$/
command=/bin/bash $HOST_PATH$$environment$_$project$/deploy_start.sh
process_name = %(process_num)d
user=$USER$
startretries=5
stopsignal=TERM
stopasgroup=true
autorestart=true
redirect_stderr=true
stdout_logfile=$supervisor_log_path$/%(program_name)s.log
stdout_logfile_maxbytes=500MB
stdout_logfile_backups=10
loglevel=info

'''


server_xml = '''<?xml version='1.0' encoding='utf-8'?>

<Server port="$shutdownport$" shutdown="SHUTDOWN">
  <Listener className="org.apache.catalina.startup.VersionLoggerListener" />
  <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />
  <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
  <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
  <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />
  <GlobalNamingResources>
    <Resource name="UserDatabase" auth="Container"
              type="org.apache.catalina.UserDatabase"
              description="User database that can be updated and saved"
              factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
              pathname="conf/tomcat-users.xml" />
  </GlobalNamingResources>
  <Service name="Catalina">
    <Connector port="$port$" address="$ip$" protocol="HTTP/1.1"
               maxThreads="500"
               minSpareThreads="50"
               maxIdleTime="60000"
               maxKeepAliveRequests="1"
               connectionTimeout="20000"
               redirectPort="8443" />
    <Connector port="$ajpport$" protocol="AJP/1.3" redirectPort="8443" />
    <Engine name="Catalina" defaultHost="localhost">
      <Realm className="org.apache.catalina.realm.LockOutRealm">
        <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
               resourceName="UserDatabase"/>
      </Realm>
      <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="false"
            xmlValidation="false" xmlNamespaceAware="false">
        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="localhost_access_log" suffix=".txt"
               pattern="%t %h [%I] %l %u %r %s %b %D[ms]" />
      </Host>
    </Engine>
  </Service>
</Server>
'''


catalina_sh = '''

#export JAVA_HOME="/opt/jdk1.8.0_45"

JAVA_OPTS="-server -Xms4000m -Xmx4000m -Xmn400m -XX:PermSize=256M -XX:MaxPermSize=256M -XX:+UseConcMarkSweepGC -XX:MaxTenuringThreshold=3 -XX:CMSInitiatingOccupancyFraction=70 -XX:CMSFullGCsBeforeCompaction=0 -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=$CATALINA_HOME/logs/dump.log.`date +%Y-%m-%d-%H-%M` -Xloggc:$CATALINA_HOME/logs/gc.log.`date +%Y-%m-%d-%H-%M`"

CATALINA_PID="$CATALINA_HOME"/temp/pid.tmp
'''
