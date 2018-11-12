#!/usr/bin/python

from __future__ import print_function
import Queue
import threading
import time
import sys
import requests
import subprocess
import MySQLdb as mysql

try:
    reload(sys)  # Python 2
    sys.setdefaultencoding('utf8')
except NameError:
    pass         # Python 3

sys.path.append("..")
from configdb import *
from config import *



notchecklist = ['']

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, q, sq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
        self.sq = sq
    def run(self):
        if self.threadID == 0:
            self.process_status()
        else:
            self.process_data()

    def process_status(self):
        while not exitFlag:
            statusqueueLock.acquire()
            if self.sq.empty():
                statusqueueLock.release()
                continue
            try:
                data = self.sq.get(True, 2)
            except Exception as err:
                statusqueueLock.release()
                print(str(err))
                continue
            statusqueueLock.release()
            print(data)
            if data['sshStatus'] == 'SSHOK':
                Exclude = ''
                for Project,Status in data['Projects'].items():
                    sql = "update `serverinfo` set `variable2`='%s',`variable5`='%s' where ip='%s' and project_name='%s';" % (Status, data['CheckTime'], data['IP'], Project)
                    #print sql
                    self.executeSQL(sql)
                    Exclude = "%s and project_name <> '%s' " %(Exclude, Project)
                sql = "update `serverinfo` set `variable2`='%s',`variable5`='%s' where ip='%s' %s;" % (data['sshStatus'], data['CheckTime'], data['IP'], Exclude)
                #print sql
                self.executeSQL(sql)
            else:
                sql = "update `serverinfo` set `variable2`='%s',`variable5`='%s' where ip='%s';" % (data['sshStatus'], data['CheckTime'], data['IP'])
                #print sql
                self.executeSQL(sql)




    def process_data(self):
        while not exitFlag:
            queueLock.acquire()
            if self.q.empty():
                queueLock.release()
                time.sleep(2)
                continue
            try:
                IP = self.q.get(True, 2)
            except Exception as err:
                queueLock.release()
                print(str(err))
                continue
            queueLock.release()

            CheckTime = time.strftime('%Y%m%d_%H:%M')
            DR = {'IP': IP, 'CheckTime': CheckTime, 'sshStatus': '', 'Projects': {} }
            try:
                shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 %s@%s "superctl status" |awk '{print $1, $2}' ''' %(exec_user, IP)
                hoststatus = self.exec_shell(shell_cmd)

                if hoststatus['status'] == 'ok':
                    DR['sshStatus'] = 'SSHOK' 
                    for s in hoststatus['log'].strip().split('\n'):
                        project = s.split()[0].split(':')[0]
                        status = s.split()[1]
                    
                        if project in DR['Projects']:
                            if status != 'RUNNING':
                                DR['Projects'][project] = status
                        else:
                            DR['Projects'][project] = status
                else:
                    DR['sshStatus'] = 'SSHFAIL' 
            except Exception as err:
                DR['sshStatus'] = 'UNKNOWN' 
                print(str(err))

            statusqueueLock.acquire()
            try:
                self.sq.put(DR, True, 2)
                if self.sq.full():
                    print('ERROR: sq Queue full')
                    self.sq.queue.clear()
            except Exception as err:
                print(str(err))
            statusqueueLock.release()


    def exec_shell(self, shell_cmd):
        s = subprocess.Popen( shell_cmd, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
        newlog, stderr = s.communicate()
        return_status = s.returncode
        if return_status == 0:
            return {'status':'ok', 'log':newlog}
        else:
            return {'status':'fail', 'log':newlog + stderr}


    def executeSQL(self, sql="select * from `serverinfo` limit 1;"):
        while True:
            try:
                self.conn.ping()
                break
            except Exception as e:
                print('warning: mysql test ping fail')
                print(str(e))
            try:
                self.conn = mysql.connect(user=user, passwd=passwd, host=host, port=port, db=dbname, connect_timeout=connect_timeout, compress=compress, charset=charset)
                self.cursor = self.conn.cursor()
                break
            except Exception as e:
                print("mysql reconnect fail ...")
                print(str(e))
                time.sleep(3)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(str(e))



queueLock = threading.Lock()
workQueue = Queue.Queue(10000)
statusqueueLock = threading.Lock()
statusQueue = Queue.Queue(10000)
threads = []
threadID = 1

for threadID in range(100):
    thread = myThread(threadID, workQueue, statusQueue)
    thread.start()
    threads.append(thread)
    threadID += 1


while True:
    if workQueue.empty():
        try:
            iplistall = requests.get(iplistallurl, timeout=2).json()
        except Exception as err:
            time.sleep(10)
            print('ERROR: iplistall URL GET fail')
            continue
        queueLock.acquire()
        try:
            for ip in iplistall:
                if ip not in notchecklist:
                    workQueue.put(ip, True, 2)
                    if workQueue.full():
                        print('ERROR: check host IP Queue %s full. clean IP Queue all' %(workQueue.qsize() ))
                        workQueue.queue.clear()
        except Exception as err:
            print(str(err))
        queueLock.release()
        time.sleep(15)
    else:
        time.sleep(3)


exitFlag = 1


for t in threads:
    t.join()
print("Exiting Main Thread")
