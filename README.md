# 前言

适合基于ssh秘钥的中小公司环境, 代码逻辑简单, 需要运维兄弟会一点python, 自定义与公司业务相关的功能,自行发挥.


   ![用户与组管理](https://github.com/liquanzhou/img/blob/master/cedardeploy/%E7%94%A8%E6%88%B7%E4%B8%8E%E7%BB%84%E7%AE%A1%E7%90%86.png "用户与组管理")
 
   ![添加项目](https://github.com/liquanzhou/img/blob/master/cedardeploy/%E6%B7%BB%E5%8A%A0%E9%A1%B9%E7%9B%AE.png "添加项目")

   ![工单](https://github.com/liquanzhou/img/blob/master/cedardeploy/%E5%B7%A5%E5%8D%95.png "工单")

   ![发布页面](https://github.com/liquanzhou/img/blob/master/cedardeploy/%E5%8F%91%E5%B8%83%E9%A1%B5%E9%9D%A2.png "发布页面")

   ![日志](https://github.com/liquanzhou/img/blob/master/cedardeploy/%E6%97%A5%E5%BF%97.png "日志")

   ![服务失败列表](https://github.com/liquanzhou/img/blob/master/cedardeploy/%E6%9C%8D%E5%8A%A1%E5%A4%B1%E8%B4%A5%E5%88%97%E8%A1%A8.png "服务失败列表")


支持编译发布的项目类型,其他项目,编译方式,可自行扩展

    nodejs 多进程 编译         supervisor

    python 多进程              supervisor

    golang        编译bin文件  supervisor

    java-tomcat   mvn编译  需要系统镜像放置一个标准的空tomcat

    java-jar      mvn编译      supervisor

    sh                         supervisor # 非nohup的前台持续运行进程

    static        发布到nginx机器,指定nginx配置

    php           先同步配置文件,在发布代码,指定nginx配置

    job           发布系统只负责同步目录,同时生成定时任务配置文件。传到远程主机cron.d目录，系统自动加载  # 下个版本更新


项目信息分三块:

    项目基础信息:  创建项目需要名称, git地址,端口,项目类型, 环境, 编译命令,检查方式等

    项目配置模板:  添加项目后,自动生成统一的模板,配置信息.比如: supervisor_conf等

    主机信息:      可配置针对不同主机独立的信息,比如: 启动进程数, 环境变量


# 安装

一.准备环境

    python 2.7

    发布机器普通用户对其他主机普通用户ssh秘钥免密码

    supervisord, 并且要所有主机加载统一目录,ssh用户有权限拷贝文件

    远程主机supervisor配置文件加载目录

    [include]

    files = supervisor_conf_dir/*.conf

    依赖包

    pip install -r requirements.txt


二.创建mysql数据库

    创建数据库,请先修改配置文件

    CREATE DATABASE `dbname` /*!40100 DEFAULT CHARACTER SET utf8 */;

    grant all on dbname.* to deployuser@localhost;


三.修改DB配置

    vim app/configdb.py


四.初始化数据库

    python manager.py db init

    python manager.py db migrate

    python manager.py db upgrade




五.配置

    目录请自行配置

    vim app/config.py


六.用户

    如果有ldap,请打开Ldap项为True

    如果没有ldap,需要手动创创建 admin 用户

    python manager.py shell

    with app.app_context():

        u = User(email='admin@163.com',username='admin',password='admin')

        db.session.add(u)

        db.session.commit()




七.启动服务

    1.deploy web启动

    2.检查服务:  app/hostscheck/hostscheck.py

    把 deploy-supervisor.conf 拷贝到 supervisord的配置目录下,修改具体程序路径和log目录,然后加载


八.服务状态报警

    如果都启动正常, 检查服务也正常启动, 可以配置定时任务报警

    * * * * * python /app/deploy/app/hostscheck/service_alarm.py >> /data/log/service_alarm.log 2>&1



# 使用

    ldap或用户登陆系统后,确保用户在配置文件的管理员列表中

    登陆后,界面空白,需要先添加组,在添加项目: 

    添加组: 用户管理 选择用户 添加组

    添加项目: 项目管理, 选择组, 选择项目语言类型, 项目名, 选择环境, git地址,分支,端口,编译方式,检查方式等. 添加后,会自动生成supervisord等模板.看情况修改

    添加主机: 项目管理, 选择组, 选择项目, 在下方添加主机名和主机ip确认. 在添加主机的同时, 会到远程创建目录,创建服务的supervisor文件,并加载

    上线服务: 上线,选择组,选择项目,勾选项目,点击更新. 确保启动发布系统的用户可以免密码拉取仓库建议添加ssh秘钥. 默认会拉取git地址对应的最新的代码,编译上线.仓库不改动,用历史最近版本上线.

    管理员不受上线时间限制,不受组限制.普通用户看不到组,可以提工单, 工单可以跳转到项目,管理员上线完,在关闭工单.也可以给普通用户对组授权,自行上线.



