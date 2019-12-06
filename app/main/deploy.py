#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
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
import MySQLdb as mysql

print('%s' % sys.path[0])

sys.path.append("..")
from configdb import *
from config import *



reload(sys);
sys.setdefaultencoding('utf8');


mdb = mysql.connect(user=user, passwd=passwd, host=host, port=port, db=dbname, charset=charset)
mdb.autocommit(True)
c = mdb.cursor()


def project_info(project):
    print(project)
    sql = "SELECT * FROM `projectinfo` WHERE project_name = '%s';" % (project)
    c.execute(sql)
    ones = c.fetchall()
    return ones[0]

def config_info(project):
    print(project)
    sql = "SELECT * FROM `project_config` WHERE project_name = '%s';" % (project)
    c.execute(sql)
    ones = c.fetchall()
    return ones[0]

def gethostname(project):
    sql = "SELECT `ip`,`hostname`,`pnum` FROM `serverinfo` WHERE project_name = '%s';" % (project)
    c.execute(sql)
    ones = c.fetchall()
    hostnameinfo = {}
    for i in ones:
        hostnameinfo[i[0]] = [i[1], int(i[2])]
    return hostnameinfo

def getworkorder(project):
    sql = "SELECT `applicant`,`remarks` FROM `workorder`  WHERE status = 'wait' and project = '%s';" % (project)
    c.execute(sql)
    ones = c.fetchall()
    if ones:
        workorderinfo = {'status':'ok', 'applicant':ones[-1][0], 'remarks':ones[-1][1]}
    else:
        workorderinfo = {'status':'null'}
    return workorderinfo



class Deploy:
    def __init__(self, project, tag, taskid, hostlist, operation, currentuser, reason):

        self.project     = project
        self.tag         = tag
        self.taskid      = taskid
        self.hostlist    = hostlist
        self.operation   = operation
        self.currentuser = currentuser
        self.reason      = reason

        pinfo  = project_info(project)
        cinfo  = config_info(project)
        self.hostnameinfo  = gethostname(project)
        self.workorderinfo = getworkorder(project)

        print(pinfo)
        print(cinfo)
        print(self.hostnameinfo)
        print(self.workorderinfo)

        self.business    = pinfo[1]
        self.environment = pinfo[2]
        self.p           = pinfo[3]
        self.Type        = pinfo[4]
        self.port        = int(pinfo[5])
        self.git         = pinfo[6]
        self.branch      = pinfo[7]


        self.make        = cinfo[1]
        self.supervisor  = cinfo[2]
        self.config      = cinfo[3]
        self.remarks     = cinfo[4]
        self.startcmd    = cinfo[5]
        self.packfile    = cinfo[6]
        self.istag       = cinfo[7]
        self.checkport   = cinfo[8]
        self.checkhttp   = cinfo[9]
        self.httpurl     = cinfo[10]
        self.httpcode    = cinfo[11]

        self.host        = 'Deploy'
        self.hostName    = 'Deploy'
        self.status      = 'ok'
        self.progress    = 0
        self.makestatus  = 'no'
        self.commitid    = ''

        self.execUser       = exec_user
        self.basicGlist     = basicGlist
        self.businessRobot  = businessRobot
        self.sreRobot       = sreRobot
        self.autotestURL    = autotestURL
        self.autolist       = autolist
        self.hostPath       = remote_host_path.rstrip('/') + '/'

        print(self.autolist)


        self.dir_path_git    = path_git.rstrip('/') + '/'    + project
        self.dir_path_log    = path_log.rstrip('/') + '/'    + project
        self.dir_path_lock   = path_lock.rstrip('/') + '/'   + project
        self.dir_path_conf   = path_conf.rstrip('/') + '/'   + project
        self.dir_path_result = path_result.rstrip('/') + '/' + project


        self.pklFile = '%s/deploy.%s.lock' %(self.dir_path_lock, project)

        self.logPath = file('%s/%s.log' % (self.dir_path_result, self.tag), 'a+')

        self.makeFun      = {   "serviceStop":         self.notexec,
                                "serviceUpdate":       self.makeUpdate,
                                "serviceFallback":     self.makeFallback,
                                "serviceFastback":     self.makeFallback,
                                "serviceExpansion":    self.makeExpansion,
                                "serviceRestart":      self.notexec
                            }


        self.remoteFun    = {   "serviceStop":         self.serviceStop,
                                "serviceUpdate":       self.serviceUpdate,
                                "serviceFallback":     self.serviceUpdate,
                                "serviceFastback":     self.serviceFastback,
                                "serviceExpansion":    self.serviceUpdate,
                                "serviceRestart":      self.serviceRestart
                            }

        self.stop         = {   "java":                self.stopJava,
                                "sh":                  self.stopSupervisor,
                                "jobs":                self.notexec,
                                "static":              self.notexec,
                                "php":                 self.notexec,
                                "go":                  self.stopSupervisor,
                                "golang":              self.stopSupervisor,
                                "python":              self.stopSupervisorPort,
                                "nodejs":              self.stopSupervisorPort
                            }

        self.rsyncCode    = {   "java":                self.rsyncJava,
                                "sh":                  self.rsyncDir,
                                "jobs":                self.rsyncDir,
                                "static":              self.rsyncDir,
                                "php":                 self.rsyncPhp,
                                "go":                  self.rsyncDir,
                                "golang":              self.rsyncGolang,
                                "python":              self.rsyncDir,
                                "nodejs":              self.rsyncDir
                            }

        self.restart      = {   "java":                self.restartJava,
                                "sh":                  self.restartSupervisor,
                                "jobs":                self.notexec,
                                "static":              self.notexec,
                                "php":                 self.notexec,
                                "go":                  self.restartSupervisor,
                                "golang":              self.restartSupervisor,
                                "python":              self.restartSupervisorPort,
                                "nodejs":              self.restartSupervisorPort
                            }


    def makeOperation(self):
        rtime = time.strftime('%Y%m%d_%H%M%S')
        self.addlog('user: %s\nhostlist: %s\noperation: %s\nproject: %s\ntaskid: %s\n' %(
                    self.currentuser, self.hostlist, self.operation, self.project, self.taskid) )
        self.addlog('Deploy System Compile Start Time: %s\n' % rtime)
        self.makeFun[self.operation]()
        rtime = time.strftime('%Y%m%d_%H%M%S')
        self.addlog('\nDeploy System Compile Done Time: %s' % rtime)
        self.updateProgress()

    def hostOperation(self):
        rtime = time.strftime('%Y%m%d_%H%M%S')
        self.addlog('%s Deploy Start Time: %s\n' % (self.hostName, rtime))
        self.addlog("PATH: %s%s/" %(self.hostPath, self.project))
        self.remoteFun[self.operation]()
        self.updateHostCommit()
        rtime = time.strftime('%Y%m%d_%H%M%S')
        self.addlog('\n%s Deploy Done Time: %s' % (self.hostName, rtime))
        self.updateProgress()

    def serviceStop(self):
        pnum = self.hostnameinfo[self.host][1]
        for port in range(self.port, self.port + pnum):
            self.removeService(port)
            self.stop[self.Type](port)

    def serviceRestart(self):
        pnum = self.hostnameinfo[self.host][1]
        for port in range(self.port, self.port + pnum):
            self.addlog('\nDel Service Start:')
            self.removeService(port)
            self.addlog('\nRestart Service:')
            self.restart[self.Type](port)
            self.addlog('\nCheck Start:')
            self.check_status(port)
            self.http_check(port)
            self.addlog('\nAutotest Start:')
            self.autotest(port)
            self.addlog('\nReg Service Start:')
            self.increaseService(port)

    def serviceUpdate(self):
        self.rsyncCode[self.Type]()
        self.serviceRestart()

    def serviceFastback(self):
        self.rsyncCode[self.Type]()
        pnum = self.hostnameinfo[self.host][1]
        for port in range(self.port, self.port + pnum):
            self.restart[self.Type](port)


    def currenthost(self, host):
        self.host = host
        try:
            self.hostName = self.hostnameinfo[self.host][0]
        except:
            self.hostName = self.host

    def addlog(self, newlog):
        self.logPath.write('\n%s' %newlog)
        self.logPath.flush()


    def updateHostCommit(self):
        if self.commitid:
            sql = "update `serverinfo` set `commitid`='%s',`updatetime`='%s' \
                           where project_name='%s' and ip='%s';   " % (
                           self.commitid, self.tag, self.project, self.host)
            try:
                c.execute(sql)
            except:
                print('ERROR: updateHostCommit execute SQL fail')
                self.done()

    def updateTaskStatus(self):
        sql = "update `updateoperation` set `status`='%s',`tag`='%s',`commitid`='%s' \
                       where project_name='%s' and taskid='%s';  " % (
                       self.status, self.tag, self.commitid, self.project, self.taskid)
        try:
            c.execute(sql)
        except Exception as err:
            print('ERROR: updateTaskStatus execute SQL fail')
            print(str(err))

    def updateProgress(self):
        self.progress = self.progress + 1
        sql = "update `updateoperation` set `progress`=%d where project_name='%s' and taskid='%s';" % (self.progress, self.project, self.taskid)
        print(sql)
        try:
            c.execute(sql)
        except Exception as err:
            print('ERROR: updateProgress execute SQL fail')
            print(str(err))

    def notice(self):
        if self.environment != 'online':
            return ''

        HL = 'hostlist:'
        for HOST in self.hostlist.split(','):
            try:
                hostname = self.hostnameinfo[HOST][0]
            except:
                hostname = HOST
            HL = HL + '  ' + hostname

        headers = {'content-type': 'application/json'}

        if self.workorderinfo['status'] == 'ok':
            content = "%s  %s:  %s\n%s\n操作人: %s\n工单人: %s\ninfo: %s" %(
                       self.project, self.operation, self.status, HL, self.currentuser, 
                       self.workorderinfo['applicant'], self.workorderinfo['remarks'])
        else:
            content = "%s  %s:  %s\n%s\n操作人: %s" %(
                       self.project, self.operation, self.status, HL, self.currentuser)

        if self.business in self.basicGlist:
            self.dingding(self.businessRobot, content)

    def expansion_notice(self):
        if self.environment != 'online':
            return ''
        headers = {'Content-Type':'application/json'}
        endtime = time.strftime('%Y-%m-%d %H:%M:%S')
        content = "%s\n%s: %s %s\nHost: %s\nReason: %s" %(
                   endtime, self.project, self.operation, self.status, self.hostlist, self.reason)

        self.dingding(self.sreRobot, content)


    def getlastokstatus(self):
        sql = "SELECT `tag`,`commitid` FROM `updateoperation`  \
                      WHERE project_name = '%s' and operation = 'serviceUpdate' and status = 'ok' \
                      order by taskid desc limit 1;" % (self.project)
        c.execute(sql)
        ones = c.fetchall()
        if ones:
            tag      = ones[0][0]
            commitid = ones[0][1]
        else:
            tag = ''
            commitid = ''
        return {'tag': tag, 'commitid': commitid}


    def exec_shell(self, shell_cmd):
        print(shell_cmd)
        s = subprocess.Popen( shell_cmd, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE  )
        newlog, stderr = s.communicate()
        return_status = s.returncode
        logs = '%s\n%s' % (newlog.strip(), stderr.strip())
        if return_status == 0:
            if logs.strip() != '':
                self.addlog(logs.strip())
            return {'status':'ok', 'log':newlog}
        else:
            self.faildone(logs)

    def ssh_shell(self, remoteCmd):
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "%s"
                    ''' %(self.execUser, self.host, remoteCmd)
        self.exec_shell(shell_cmd)

    def ssh_rsync(self, localPath, remotePath):
        shell_cmd = '''rsync -az --delete -e "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2" %s/ %s@%s:%s/  > /dev/null
                    ''' %(localPath, self.execUser, self.host, remotePath)
        self.exec_shell(shell_cmd)

    def dingding(self, Robot, content):
        data = {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
        try:
            r = requests.post(url=Robot, data=json.dumps(data), headers=headers, timeout=2).json()
        except Exception as err:
            print('ERROR: notice dingding api error. %s' %(str(err)))

    def done(self):
        self.updateTaskStatus()
        self.notice()
        if self.operation == 'serviceExpansion':
            self.expansion_notice()
        try:
            os.remove(self.pklFile)
        except:
            pass
        self.del_backup_operation()
        self.logPath.close()
        if self.status == 'ok':
            sys.exit(0)
        else:
            sys.exit(1)

    def faildone(self, log=''):
        self.addlog('ERROR: %s' %(log))
        self.status = 'fail'
        self.done()

    def notexec(self, port = None):
        pass

    def makeUpdate(self):
        self.addlog('\nGit Code update:')
        self.code_update()
        if self.checkcommitid():
            self.addlog('\nCode Compile:')
            self.make_operation()
            self.makestatus = 'yes'
            self.tag_operation()
            self.addlog('\nVersion Backup:')
            self.backup_operation()
            self.write_commitid()
        else:
            self.addlog('INFO: not make code')
        self.addlog('\nUpdate Config:')
        self.build_file_operation()
        self.addlog('INFO:  tag: %s' %(self.tag))
        self.addlog('INFO:  commitid: %s' %(self.commitid))

    def makeFallback(self):
        self.check_backup_operation()
        self.local_commitid()

    def makeExpansion(self):
        self.tag = self.getlastokstatus()['tag']
        if self.tag == '':
            self.faildone('getlastokstatus. not update ok. ')
        self.check_backup_operation()
        self.local_commitid()

    def code_update(self):
        if self.Type == 'go':
            shell_cmd = ''' rm -rf %s/%s ; git  clone  --depth=1 -b %s %s %s/%s && cd %s/%s && git log -n 1 --stat
                        ''' %(self.dir_path_git, self.project, self.branch, self.git, self.dir_path_git, self.project, self.dir_path_git, self.project )
            self.exec_shell(shell_cmd)
        elif os.path.isdir('%s/%s' %(self.dir_path_git, self.project) ):
            shell_cmd = "cd %s/%s && git remote -v |grep fetch |awk '{print $2}'" %(self.dir_path_git, self.project)
            Result = self.exec_shell(shell_cmd)
            localGit = Result['log'].strip()
            if localGit == self.git:
                shell_cmd = ''' cd %s/%s && git reset --hard && git gc && git remote prune origin \
                                      && git fetch && git checkout %s && git reset --hard origin/%s \
                                      && git submodule init && git submodule update \
                                      && git log -n 1 --stat
                            '''  %(self.dir_path_git, self.project, self.branch, self.branch)
                self.exec_shell(shell_cmd)
            else:
                shell_cmd = 'rm -rf %s/%s' %(self.dir_path_git, self.project)
                self.addlog(shell_cmd)
                self.exec_shell(shell_cmd)
                shell_cmd = 'git clone  %s %s/%s' %(self.git, self.dir_path_git, self.project)
                self.addlog(shell_cmd)
                self.exec_shell(shell_cmd)
        else:
            shell_cmd = 'git clone  %s %s/%s' %(self.git, self.dir_path_git, self.project)
            self.addlog(shell_cmd)
            self.exec_shell(shell_cmd)

        shell_cmd = "cd %s/%s && git rev-parse HEAD" %(self.dir_path_git, self.project)
        Result = self.exec_shell(shell_cmd)
        self.commitid = Result['log'].strip()[0:8]


    def checkcommitid(self):
        laststatus   = self.getlastokstatus()
        lastcommitid = laststatus['commitid']
        lasttag      = laststatus['tag']

        if self.commitid == lastcommitid:
            self.tag = lasttag
            self.addlog('lastCommitId: %s' %(self.commitid) )
            self.addlog('lasttag: %s' %(self.tag) )
            return False
        else:
            self.addlog('newCommitId: %s' %(self.commitid) )
            return True


    def local_commitid(self):
        self.commitid = os.popen('cat  %s/%s-%s/commit.id' %(
                                  self.dir_path_git, self.project, self.tag )).read().strip()
        self.addlog('localCommitId: %s' %(self.commitid))


    def build_file_operation(self):
        if not os.path.isdir('%s/%s-%s/' %(self.dir_path_git, self.project, self.tag)):
            self.faildone('%s/%s-%s/ directory does not exist. build_file_operation' 
                      %(self.dir_path_git, self.project, self.tag) )

        if self.Type == 'golang':
            shell_cmd = "cd %s/%s-%s && rm -rf  deploy-etc/ deploy-bin/etc && mkdir -p deploy-bin && git clone --depth=1 %s deploy-etc  && cp -a deploy-etc/etc  deploy-bin/etc " %(self.dir_path_git, self.project, self.tag, self.supervisor.strip() )
            self.exec_shell(shell_cmd)
            shell_cmd = '''cd %s/%s-%s && cp -a startdata libs deploy-bin/ ''' %(
                                  self.dir_path_git, self.project, self.tag)
            print(os.popen(shell_cmd).read())
            shell_cmd = '''cd %s/%s-%s && cp -a deploy-etc deploy-bin/etc 
                        ''' %(self.dir_path_git, self.project, self.tag)
            print(os.popen(shell_cmd).read())

            self.addlog('---------------------------\n%s\n---------------------------' %self.supervisor)
        else:
            pass


    def make_operation(self):
        if self.make:
            make_start_time = time.strftime('%Y-%m-%d %H:%M:%S')
            if self.Type == 'golang':
                shell_cmd = '''cd %s/%s && . $HOME/.bashrc  \
                                      && sh deploy_build.sh %s %s
                            ''' %(self.dir_path_git, self.project, self.project, self.make)
            else:
                shell_cmd = "cd %s/%s  && . $HOME/.bashrc && %s" %(
                             self.dir_path_git, self.project, self.make)
            self.exec_shell(shell_cmd)
            make_done_time = time.strftime('%Y-%m-%d %H:%M:%S')
            self.addlog('make_start_time: %s' %(make_start_time))
            self.addlog('make_done_time: %s' %(make_done_time))


    def tag_operation(self):
        if self.istag == 'yes':
            shell_cmd = "cd %s/%s && git tag %s-%s && git push origin --tags" %(
                           self.dir_path_git, self.project, self.project, self.tag)
            self.exec_shell(shell_cmd)

    def write_commitid(self):
        self.addlog('INFO: write_commitid')
        shell_cmd = 'echo %s >  %s/%s-%s/commit.id' %(
                     self.commitid, self.dir_path_git, self.project, self.tag)
        self.exec_shell(shell_cmd)

    def backup_operation(self):
        bak_start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        shell_cmd = '''rsync -a --exclude .git/ --delete %s/%s/  %s/%s-%s/
                    ''' %(self.dir_path_git, self.project, self.dir_path_git, self.project, self.tag)
        self.exec_shell(shell_cmd)
        bak_done_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.addlog('bak_start_time: %s' %(bak_start_time))
        self.addlog('bak_done_time : %s' %(bak_done_time))


    def del_backup_operation(self):
        if self.makestatus == 'yes':
            if self.status == 'ok':
                num = 5
                if self.environment == 'online':
                    num = 9
                shell_cmd = '''ls -dr %s/%s-%s-20* 2>/dev/null |awk "NR>%s{print $1}" |xargs -i rm -rf {} 
                            ''' %(self.dir_path_git, self.project, self.project.split('_')[0], num)
            else:
                shell_cmd = 'rm -rf %s/%s-%s/' %(self.dir_path_git, self.project, self.tag)
            self.exec_shell(shell_cmd)


    def check_backup_operation(self):
        if os.path.isdir('%s/%s-%s/' %(self.dir_path_git, self.project, self.tag)):
            self.addlog('INFO: %s/%s-%s directory does exist. check_backup_operation' 
                      %( self.dir_path_git, self.project, self.tag) )
        else:
            self.faildone('%s/%s-%s directory does not exist. check_backup_operation' 
                      %( self.dir_path_git, self.project, self.tag) )

    def check_status(self, port = None):
        if port is None:
            port = self.port
        if self.checkport == 'yes':
            i = 0
            results = ''
            while i < 60:
                s = socket.socket()
                s.settimeout(1)
                try:
                    portstatus = s.connect_ex((self.host, port ))
                    print('portstatus %s: %s' %(i, portstatus))
                    #self.addlog('portstatus %s: %s' %(i, portstatus))
                    if portstatus == 0:
                        results = 'ok'
                        time.sleep(5)
                        break
                    else:
                        results = 'fail'
                except Exception as err:
                    self.addlog(str(err))
                    results = 'fail'
                s.close()
                i = i + 1
                time.sleep(2)

            if results == 'ok':
                self.addlog('INFO: check ip port up: %s:%s' %(self.host, port))
            else:
                self.faildone('check ip port down: %s:%s' %(self.host, port))

    def http_check(self, port = None):
        if port is None:
            port = self.port
        if self.checkhttp == 'get':
            i = 0
            results = ''
            httpcontent = ''
            url = 'http://%s:%s%s' %(self.host, port, self.httpurl)
            while i < 30:
                try:
                    r = requests.get(url,timeout=2)
                    httpstatus = r.status_code
                    httpcontent = r.content

                    if httpstatus == int(self.httpcode):
                        results = 'ok'
                        time.sleep(1)
                        break
                    else:
                        results = 'fail'
                except:
                    httpstatus = 0
                    results = 'fail'
                i = i + 1
                time.sleep(1)

            if results == 'ok':
                self.addlog('INFO: http check %s ok. http status code: %s \n%s\n' %(
                             url, httpstatus, httpcontent))
            else:
                self.faildone('http check %s fail. http status code: %s \n%s\n' %(
                               url, httpstatus, httpcontent))


    def stopSupervisor(self, port = None):
        remoteCmd = 'supervisorctl stop %s:' %(self.project)
        self.ssh_shell(remoteCmd)
    def stopSupervisorPort(self, port = None):
        remoteCmd = 'supervisorctl stop %s:%s' %(self.project, port)
        self.ssh_shell(remoteCmd)
    def stopJava(self, port = None):
        remoteCmd = '%s/%s/bin/catalina.sh stop 30 -force;' %(self.hostPath, self.project)
        self.ssh_shell(remoteCmd)


    def restartSupervisor(self, port = None):
        remoteCmd = 'supervisorctl stop %s: ;supervisorctl update;supervisorctl start %s:' %(self.project, self.project)
        self.ssh_shell(remoteCmd)
    def restartSupervisorPort(self, port = None):
        if port is None:
            port = self.port
        remoteCmd = 'supervisorctl stop %s:%s ;supervisorctl update;supervisorctl start %s:%s' %(self.project, port, self.project, port)
        self.ssh_shell(remoteCmd)
    def restartJava(self, port = None):
        shell_cmd = '''"%s/%s/bin/catalina.sh stop 30 -force; \
                       rm -rf %s/%s/webapps/ROOT %s/%s/webapps/%s.war ; \
                       %s/%s/bin/catalina.sh start; sleep 1; \
                       tail -5 $s/%s/logs/catalina.out" 
                    ''' %(self.hostPath, self.project, self.hostPath, self.project, self.hostPath, 
                          self.project, self.hostPath, self.project, self.project, self.hostPath, self.project)
        self.ssh_shell(remoteCmd)



    def rsyncDir(self):
        remoteCmd = 'mkdir -p %s/%s' %(self.hostPath, self.project)
        self.ssh_shell(remoteCmd)
        localPath  = '%s/%s-%s/' %(self.dir_path_git, self.project, self.tag)
        remotePath = '%s/%s' %(self.hostPath, self.project)
        self.ssh_rsync(localPath, remotePath)
    def rsyncPhp(self):
        remoteCmd = 'mkdir -p %s/%s/conf' %(self.hostPath, self.project)
        self.ssh_shell(remoteCmd)
        localPath  = '%s/%s-%s/conf/' %(self.dir_path_git, self.project, self.tag)
        remotePath = '%s/%s/conf/' %(self.hostPath, self.project)
        self.ssh_rsync(localPath, remotePath)

        localPath  = '%s/%s-%s/' %(self.dir_path_git, self.project, self.tag)
        remotePath = '%s/%s/' %(self.hostPath, self.project)
        self.ssh_rsync(localPath, remotePath)

    def rsyncGolang(self):
        remoteCmd = 'mkdir -p %s/%s' %(self.hostPath, self.project)
        self.ssh_shell(remoteCmd)
        localPath  = '%s/%s-%s/deploy-bin/' %(self.dir_path_git, self.project, self.tag)
        remotePath = '%s/%s/' %(self.hostPath, self.project)
        self.ssh_rsync(localPath, remotePath)
    def rsyncJava(self):
        war_path = config4.split(' ')[0].strip().split('\n')[0]
        shell_cmd = '''scp -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s/%s-%s/%s  %s@%s:%s/%s/webapps/ROOT.war  > /dev/null  
                    ''' %(self.dir_path_git, self.project, self.tag, war_path, self.execUser, self.host, self.hostPath, self.project)
        self.exec_shell(shell_cmd)



    def removeService(self, port = None):
        if port is None:
            port = self.port
        if self.operation == 'serviceExpansion':
            return 'not removeService'

        if self.Type == 'golang':
            consul_port = port - 3000
            consul_srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            consul_srv_sock.settimeout(2)
            try:
                consul_srv_sock.connect((self.host, consul_port ))
                try:
                    self.addlog(time.strftime('%Y-%m-%d %H:%M:%S'))
                    consul_srv_sock.send('on offline\n')
                    result = consul_srv_sock.recv(1024).strip()
                    if result == 'OK':
                        self.addlog('INFO: consul disable %s %s:%s %s' %(self.project, self.host, consul_port, result))
                        time.sleep(20)
                        self.addlog(time.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        self.addlog('WARN: consul disable %s %s:%s %s' %(self.project, self.host, consul_port, result))
                except:
                    self.addlog('WARN: %s %s:%s socket send error' %(self.project, self.host, consul_port))
            except:
                self.addlog('WARN: %s %s:%s Connect timeout' %(self.project, self.host, consul_port))


    def increaseService(self, port = None):
        if port is None:
            port = self.port
        if self.checkport == 'yes':
            pass

    def autotest(self, port = None):
        if port is None:
            port = self.port
        if self.environment != 'online':
            self.addlog('INFO: not auto test\n')
            return 'not auto test'
        if self.operation == 'serviceFallback':
            self.addlog('INFO: serviceFallback not auto test\n')
            return 'INFO: serviceFallback not auto test'
        if self.project in self.autolist:
            data = {'biz':self.project, 'host': self.host, 'port': self.port, 'way':1}
            try:
                r = requests.post(self.autotestURL, data=json.dumps(data)).json()
                self.addlog(r['data'])
                if r['data'] == 'pass':
                    self.addlog('INFO: auto test OK\n')
                    return 'ok'
                else:
                    self.faildone('auto test Fail.\nError details: %s' %(r['url_list']) )
            except Exception as err:
                self.faildone('auto test Fail. QA api Fail \n%s' % str(err))




if __name__ == "__main__":

    project = sys.argv[1]
    tag = sys.argv[2]
    taskid = sys.argv[3]
    hostlist = sys.argv[4]
    operation = sys.argv[5]
    currentuser = sys.argv[6]
    reason = sys.argv[7]


    dp=Deploy(project, tag, taskid, hostlist, operation, currentuser, reason)
    dp.makeOperation()

    for host in hostlist.split(','):
        dp.currenthost(host)
        dp.hostOperation()

    dp.done()



