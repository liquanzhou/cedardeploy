#!/usr/bin/env python
# coding: utf-8

# 发布系统本地配置
# 管理员用户 用户名
adminuser = ['xuesong', 'admin']
# 发布系统执行编译及ssh用户
exec_user = 'work'
# 发布系统git仓库存放目录
project_path = '/data1/deploy_project'
# 发布系统本地log目录
log_path = '/data/log'
# 发布任务锁文件存放位置 lock_path/deploy.project.lock
lock_path = '/tmp'

#ldap: True    用户登陆: False
#Ldap=True
Ldap=False
LDAP_HOST = "ldap://172.10.1.233:389"
LDAP_BASE = "ou=People,dc=xc,dc=cn"


# 远程发布目录
remote_host_path = '/app/project/'

# 使用supervisord管理的进程 项目类型
supervisord_list = ['sh', 'go', 'golang', 'python', 'nodejs', 'java-jar']
# 远程主机supervisor配置文件目录
# [include] 
# files = supervisor_conf_dir/*.conf
supervisor_conf_dir = '/app/supervisor/conf/conf.d/'
# 远程主机supervisor存放日志目录, 没有服务无法启动
supervisor_log_path = '/data/logs/supervisor/'


# 管理员菜单列表
adminpagelist = [['online','上线'],['project_admin','项目管理'],['online_log','发布日志'],['statistics','统计'],['useradmin','用户管理'],['workorderweb','上线工单'],['hostmanage','主机管理']]
# 普通用户菜单列表
userpagelist = [['online','上线'],['project_admin','项目管理'],['online_log','发布日志'],['statistics','统计'],['workorderweb','上线工单']]


# 运维钉钉通知地址
sreRobot = 'https://oapi.dingtalk.com/robot/send?access_token=8a662b74fdce5c905b'
# 业务线钉钉通知
businessRobot = 'https://oapi.dingtalk.com/robot/send?access_token=cd4ebe40'
# 发钉钉通知的组 组名
basicGlist = ['op-ad', 'op-ab', 'ff-aa']


# 检查服务状态时,获取项目信息
#projectinfoallurl = 'http://127.0.0.1:6000/projectinfoall'
#hostlistallurl = 'http://127.0.0.1:6000/hostlistall'
# 检查服务状态时,获取主机列表
iplistallurl = 'http://127.0.0.1:6000/iplistall'
# 检查失败不报警的项目  项目名
filterList = ['online_testproject']
# 检查失败不报警的主机列表 ip
notcheckhost = ['172.10.0.172', '172.20.20.80']


# 不限制上线时间的组 组名
unlimit = ['offline', 'sre', 'op', 'web']
unlimitProject = ['test_project']

autotestURL = 'http://10.10.10.10/deploy/check'
# 需要自动测试的项目 项目名
autolist = ['online_testproject', 'online_testproject2']


