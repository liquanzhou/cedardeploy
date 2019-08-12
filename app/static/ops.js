
//这个是全局的定时器。
var timeout ;
var timeout1 ;
var timeout2 ;


$("body").on('click', '#open_add_project', function(){
    var status = $('#project_div').attr('status')
    if (status == 'close') {
        push_add_project_table()
        $('#project_div').attr('status','open')
        $('#add_host_table').html("");
        $('#host').html("");
    }else{
        $('#project_div').html("");
        $('#project_div').attr('status','close');
    }
});

$("body").on('click', '#del_project', function(){
    var project = $('#ipt_project').val()
    if (confirm('请确认删除项目及关联主机信息: '+project)) {
        var param = {
            project: project
        }
        $.post('/del_project', param, function(data){
            alert("删除项目 "+project+"  status: "+data.status+" log: "+data.log);
            if (data.status == 'ok') {
                project_list();

                $('#project_div').html("");
                $('#add_host_table').html("");
                $('#host').html("");
            }
        }, 'json');
    };
});


function push_add_host_table(p){
    var project = p
    var param = {
        project: project
    }
    $.getJSON('/project_info', param, function(data){
        var htm=['<table class="table table-hover">'];
        htm.push('<thead><tr><th>hostname</th><th >ip</th><th >pnum</th><th >env</th><th >add host</th></thead>');
        htm.push('<tr>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_hostname" placeholder="host-01" value="">'+'</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_ip" placeholder="10.10.10.10" value="">'+'</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_pnum" placeholder="" value="1">'+'</td>');
        htm.push('<td>'+'<input type="text" class="form-control" id="add_env" placeholder="" value="">'+'</td>');
        htm.push('<td><button id="add_host" class="btn btn-small btn-success" project="'+project+'" >确认添加</button></td>');
        htm.push('</tr>');
        htm.push('</table>');
        $('#add_host_table').html(htm.join(''));
    })
};


$("body").on('click', '#open_add_host', function(){
    var project = $('#open_add_host').attr('project')
    var status = $('#open_add_host').attr('status')
    if (status == 'close') {
        push_add_host_table(project)
        $('#open_add_host').attr('status','open')
    }else{
        $('#add_host_table').html("");
        $('#open_add_host').attr('status','close')
    }
});


$("body").on('click', '#open_edit_host', function(){
    var project = $('#open_edit_host').attr('project')
    var status = $('#open_add_host').attr('status')
    if (status == 'close') {
        push_edit_host_table(project)
        $('#open_add_host').attr('status','open')
    }else{
        $('#add_host_table').html("");
        $('#open_add_host').attr('status','close')
    }
});


$("body").on('click', '#add_project', function(){
    if (confirm('请确认项目信息')) {
        var add_business = $('#add_business').val()
        var add_environment = $('#add_environment').val()
        var add_project = $('#add_nproject').val()
        var add_type = $('#add_type').val()
        var add_port = $('#add_port').val()
        var add_git = $('#add_git').val()
        var add_branch = $('#add_branch').val()

        if(!add_business ){
            alert('business null');
            return false;
        }

        if(!add_environment ){
            alert('environment null');
            return false;
        }
        if(!add_branch ){
            alert('git branch null');
            return false;
        }
        if(!add_project ){
            alert('project null');
            return false;
        }
        if(!add_type){
            alert('type null');
            return false;
        }
        if(!add_git){
            alert('git addr null');
            return false;
        }
        if(add_type == 'nodejs'){
            if(add_port < 3000 || add_port >5000){
                alert('python port [3000 - 5000]');
                return false;
            }
        }

        var param = {
            business:add_business,
            environment: add_environment,
            project: add_project,
            type: add_type,
            port: add_port,
            git: add_git,
            branch: add_branch
        }

        $.post('/add_project', param, function(data){
            alert(data.status+"  "+data.log);
            if(data.status == 'ok'){
                $('#project_div').html("");
                $('#project_div').attr('status','close')
                project_list();
            }
        }, 'json');
    };
});



$("body").on('click', '#update_project', function(){
    if (confirm('请确认项目信息')) {
        var add_business    = $('#add_business').val()
        var add_environment = $('#add_environment').val()
        var add_project     = $('#add_nproject').val()
        var add_type        = $('#add_type').val()
        var add_port        = $('#add_port').val()
        var add_git         = $('#add_git').val()
        var add_branch      = $('#add_branch').val()

        if(!add_environment){
            alert('environment null');
            return false;
        }
        if(!add_branch){
            alert('git branch null');
            return false;
        }
        if(!add_project){
            alert('project null');
            return false;
        }
        if(!add_type){
            alert('type null');
            return false;
        }
        if(!add_git){
            alert('git addr null');
            return false;
        }
        var param = {
            business: add_business,
            environment: add_environment,
            project: add_project,
            type: add_type,
            port: add_port,
            git: add_git,
            branch: add_branch,
        }

        $.post('/update_project', param, function(data){
            alert(data.status+"  "+data.log);
            if(data.status == 'ok'){
                $('#project_div').html("");
                $('#project_div').attr('status','close')
                project_list();
            }
        }, 'json');
    };
});



function push_add_project_table(){

    $.getJSON('/group_list', function(data){

    var htm=['<table class="table table-hover ">'];

    htm.push('<tr>');
    htm.push('<td width="120" align="right">Business line:</td>');
    htm.push('<td>'+'<select class="form-control" id="add_business">');
    for(var i=0,len=data.length; i<len; i++){
        htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
    }
    htm.push('</select></td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">environment:</td>');
    htm.push('<td>'+'<select class="form-control" id="add_environment"><option value="test" selected = "selected">test</option><option value="online">online</option><option value="pre" >pre</option><option value="beta">beta</option><option value="dev">dev</option><option value="offline">offline</option><option value="qa">qa</option><option value="job">job</option></select>'+'</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">project:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_nproject" placeholder="api" value="">'+'</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">type:</td>');
    htm.push('<td>'+'<select class="form-control" id="add_type"><option value="golang" selected = "selected">golang</option><option value="go">go-bin</option><option value="php">php</option><option value="python">python</option><option value="static">static</option><option value="jobs">jobs</option><option value="nodejs">nodejs</option><option value="sh">sh</option></select>'+'</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">port:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_port" placeholder="go port[8000-10000]  nodejs port[3000-5000] python port [5000-7000]" value="">'+'</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">git:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="git://github.com/sre/op.git" value="">'+'</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td width="120" align="right">branch:</td>');
    htm.push('<td>'+'<input type="text" class="form-control" id="add_branch" placeholder="master" value="master">'+'</td>');
    htm.push('</tr>');

    htm.push('<tr>');
    htm.push('<td></td>');
    htm.push('<td><button id="add_project" class="btn btn-small btn-success" >确认添加</button></td>');
    htm.push('</tr>');
    htm.push('</table>');

    $('#project_div').html(htm.join(''));

    })
};


$("body").on('click', '#add_host', function(){
    if (confirm('确认提交？')) {
        var add_hostname = $('#add_hostname').val()
        var add_ip       = $('#add_ip').val()
        var add_project  = $('#add_host').attr('project')
        var add_pnum     = $('#add_pnum').val()
        var add_env      = $('#add_env').val()
        var param = {
            hostname: add_hostname,
            host: add_ip,
            project: add_project,
            pnum: add_pnum,
            env: add_env
        }

        $.post('/add_host', param, function(data){
            host_list_table(add_project)
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});


$("body").on('click', '#add_group', function(){
    if (confirm('确认提交？')) {
        var addgroupname = $('#addgroupname').val()
        var param = {
            addgroupname: addgroupname,
        }
        $.post('/add_group', param, function(data){
            group_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});


$("body").on('click', '#del_group', function(){
    if (confirm('确认删除服务组？')) {
        var selectgroup = $('#selectgroup').val()
        var param = {
            selectgroup: selectgroup,
        }
        $.post('/del_group', param, function(data){
            group_list_all()
            alert(data.status+"  "+data.log);
        }, 'json');
    };
});


$("body").on('click', '#add_servergroup', function(){
    if (confirm('确认提交？')) {
        var username = $('#current_user').val()
        var servicegroup = $('#add_server_group').val()
        var permissions = $('#add_permissions').val()
        var param = {
            username: username,
            servicegroup: servicegroup,
            permissions: permissions,
        }
        $.post('/adduserservicegroup', param, function(data){
            alert(data.status+"  "+data.log);
            userservicegrouplist(username);
            servergroup_list_all()
        }, 'json');
    };
});



$("body").on('click', '#delete_servergroup', function(){
    if (confirm('确认提交？')) {
        var username = $(this).attr('username')
        var servicegroup = $(this).attr('servergroup')
        var param = {
            user: username,
            servicegroup: servicegroup,
        }
        $.post('/deleteuserservicegroup', param, function(data){
            alert(data.status+"  "+data.log);
            userservicegrouplist(username);
        }, 'json');
    };
});



$("body").on('click', '#delete_user', function(){
    if (confirm('确认提交？')) {
        var username = $(this).attr('username')
        var param = {
            deleteuser: username,
        }
        $.post('/delete_user', param, function(data){
            alert(data.status+"  "+data.log);
            user_list();
        }, 'json');
    };
});



$("body").on('click', '#add_user', function(){
    if (confirm('确认提交？')) {
        var username = $('#addusername').val()
        var password = $('#addpassword').val()
        var param = {
            adduser: username,
            password: password,
        }
        $.post('/add_user', param, function(data){
            alert(data.status+"  "+data.log);
            user_list();
        }, 'json');
    };
});



$("body").on('click', '#update_host', function(){
    var num      = $(this).attr('i')
    var project  = $(this).attr('project')
    var hostname = $('#hostname'+num).val()
    var hostip   = $('#hostip'+num).val()
    var pnum     = $('#pnum'+num).val()
    var env      = $('#env'+num).val()

    if (confirm('请确认更新: '+host)) {
        var param = {
            hostip:    hostip,
            hostname:  hostname,
            project:   project,
            pnum:      pnum,
            env:       env
        }
        $.post('/update_host', param, function(data){
            host_list_table(project)
            alert(data.status+"  "+data.log);
        }, 'json');
    }
});


$("body").on('click', '#del_host', function(){
    var host = $(this).attr('host')
    var project = $(this).attr('project')
    if (confirm('请确认删除: '+host)) {
        var param = {
            host:    host,
            project: project,
        }
        $.post('/del_host', param, function(data){
            host_list_table(project)
            alert(data.status+"  "+data.log);
        }, 'json');
    }
});


$("body").on('click', '#deploy_config', function(){
    var deploy_config_host = $(this).attr('host')
    var deploy_config_project = $(this).attr('project')
    if (confirm('警告: supervisor配置文件改动,更新或重启生效  '+deploy_config_host)) {
        var param = {
            host:    deploy_config_host,
            project: deploy_config_project,
        }
        $.post('/deploy_config', param, function(data){
            host_list_table(deploy_config_project)
            alert('deploy config '+deploy_config_host+' status: '+data['status']);
        }, 'json');
    }
});


$("#back_submit").on('click', function(){
    var  p = $('#ipt_project').val()
    if (p == undefined){
        alert('project_name null');
        return false;
    }
    var fastback = $('#fastback').val()
    if (fastback == 'yes'){
        if (confirm('快速回滚: '+ p +'？ 仅限在有故障时紧急操作,不是平滑操作,服务接口会有大量报错,也不做任何检查.')) {
            var operation = 'serviceFastback'
        }else{
            return false;
        };
    }else{
        var operation = 'serviceFallback'
    }

    var param = {
        project: p,
        operation: operation,
        tag: $('#select_tag').val(),
    };

    $.getJSON('/lock_check', param, function(data){
        if(data['status'] == "ok"){
            if (confirm('请确认回滚'+ p +'？')) {
                updateonline(param)
            };
        }else{
            alert(data['user'] + '正在操作，请勿重复执行！')
        }
    });
});



$("body").on('click', '#btn_submit', function(){
    var  p = $('#ipt_project').val()
    if (p != undefined){
        var param = {
            operation: 'serviceUpdate',
            project: p,
        };
        $.getJSON('/lock_check', param, function(data){
            if(data['status'] == "ok"){
                if (confirm('请确认更新' + p + '并重启服务!')) {
                    updateonline(param)
                    online_tag(p)
                    current_tag(p)
                };
            }else{
                alert(data['user'] + '正在操作' + p + '，请勿重复执行！')
            }
        });
    }
    else{
        alert('project_name null');
    };
});


$("#restart_submit").on('click', function(){
    var  p = $('#ipt_project').val()
    if (p != undefined){
        var param = {
            operation: 'serviceRestart',
            project: p,
        };
        $.getJSON('/lock_check', param, function(data){
            if(data['status'] == "ok"){
                if (confirm('请确认重启'+ p +'服务!')) {
                    updateonline(param)
                };
            }else{
                alert(data['user'] + '正在操作，请勿重复执行！')
            }
        });
    }
    else{
        alert('project_name null');
    };
});



function updateonline(param){
    if (param['operation'] == 'serviceStop'){
        var num = 1;
    } else {
        var chks = $('.hostList input:checkbox:checked');
        var num = chks.length;
        if(num==0){
            alert('host list null')
            return
        }
        var _arr=[];
        for(var i=0,len=num; i<len; i++){
            _arr.push(chks[i].value) ;
        }
        param.client = _arr.join(",");
    }

    console.log(param);

    $.post('/deploy', param, function(data){
        $("#resDiv").html( "operation:&nbsp;"+data.operation+
            "<br>project:&nbsp;"+data.project+
            "<br>hostlist:&nbsp;"+data.hostlist+
            "<br>taskid:&nbsp;"+data.taskid+
            "<br>tag:&nbsp;"+data.tag+
            "<br>status:&nbsp;"+data.status+
            "<br>logout:&nbsp;"+data.output
            );
        if(data.status == 'wait'){
            if(timeout){clearInterval(timeout)};
            timeout = setInterval(function(){
                next(data.taskid, num);
            },4000);
            $('#cnt').html("");
        } else {
            alert(data.status + '  ' + data.output)
        };
    }, 'json');
};


function pagelist(){
    $.getJSON('/pagelist',  function(data){
        var htm=['<ul class="nav nav-pills navbar-left" role="tablist">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<li role="presentation"><a class="presentationLink" href="/'+data[i][0]+'">'+data[i][1]+'</a></li>');
        }
        htm.push('</ul>');
        $('#pagelist').html(htm.join(''));
    });
};



function project_list(p){

    var selectgroup = $('#selectgroup').val()
    var functype = $('#leftDiv').attr('path')
    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'group', selectgroup)
        $v.attr('href', newHref)
    })
    var param = {
        group: selectgroup,
        functype: functype
    }

    $.getJSON('/project', param , function(data){

        var htm=[''];
        $.each(data, function(g, projectlist){
            htm.push('<a href="#'+g+'" class="nav-header menu-first collapsed" data-toggle="collapse" aria-expanded="false"><i class="icon-user-md icon-large"></i><h4>'+g+'</h4></a>');
            htm.push('<ul id="'+g+'" class="collapse in" >');

            var h=projectlist.sort();
            for(var i=0,len=h.length; i<len; i++){

                if(functype == "online"){
                    htm.push('<li ><a id="'+h[i]+'" class="host_list" style="cursor:pointer;" data-project="'+h[i]+'"><i class="icon-user"></i>');
                }
                if(functype == "project_admin"){
                    htm.push('<li ><a id="'+h[i]+'" class="host_list_admin" style="cursor:pointer;" data-project="'+h[i]+'"><i class="icon-user"></i>');
                }
                if(functype == "online_log"){
                    htm.push('<li ><a id="'+h[i]+'" class="online_log_time" style="cursor:pointer;" data-project="'+h[i]+'"><i class="icon-user"></i>');
                }
                htm.push('<p class="text-success">'+h[i]+'</p>');
                htm.push('</a></li>');
            }
            htm.push('</ul><br>');
        })
        $('#project').html(htm.join(''));
        $('#project_div').attr('status','close');

        if (p != undefined ) {
            if(functype == "online"){
                host_list_push(p);
            }
            if(functype == "project_admin"){
                console.log('project_admin');
                $('p').css('background','');
                $($('[data-project="'+p+'"]').find('p')[0]).css({"backgroundColor":"#C1FFC1"});
            }
        }
        jump()
    });
};

function jump(){
    var id = parseQuery().project
    if(id){
        var el = $('#' + id)[0]
        el.scrollIntoView({behavior: 'smooth'})
    }
};

function group_list(){

    var url=window.location.search.substr(1).split("&")
    var avgr = new Array();

    for (var i = 0; i < url.length; i++){
        avgr[url[i].split('=')[0]] = url[i].split('=')[1];
    }
    $.getJSON('/group_list', function(data){
        var htm=['<select class="form-control" id="selectgroup" onchange="project_list()">'];
        for(var i=0,len=data.length; i<len; i++){
            if (avgr['group'] == data[i]){
                htm.push('<option value="'+data[i]+'" selected="selected">'+data[i]+'</option>');
            } else{
                htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
            }
        }
        htm.push('</select>');
        $('#group').html(htm.join(''));
        project_list(avgr['project']);
    })
};

function group_list_all(){
    $.getJSON('/group_list_all', function(data){
        var htm=['<select class="form-control" id="selectgroup">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#groupnamediv').html(htm.join(''));
    })
};

function user_list(){
    $.getJSON('/user_list', function(data){
        var htm=['<ul type="disc">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<li><a class="userlist" username="'+data[i]+'">'+data[i]+'</a></li>');
        }
        htm.push('</ul>');
        $('#user_list').html(htm.join(''));
    })
};



$("body").on('click', '.userlist', function(){
    var username = $(this).attr('username')
    userservicegrouplist(username)
    servergroup_list_all()
});


function userservicegrouplist(username){
    var param = {
        user: username
    }

    $.getJSON('/userservicegrouplist', param, function(data){
        var htm=['<table class="table table-hover">'];
        htm.push('<thead><tr><th>username</th><th>server group</th><th>permissions</th><th>operation</th></thead>');
        htm.push('<tr>');
        htm.push('<td>'+'<input type="text" readonly="true" id="current_user" class="form-control"  value="'+username+'">'+'</td>');
        htm.push('<td>'+'<div id="usergroupnamediv" class="sidebar-menu"></div>'+'</td>');
        htm.push('<td>'+'<select class="form-control" id="add_permissions"><option value="developer"  selected="selected">developer</option><option value="config">config</option><option value="online">online</option></select>'+'</td>');
        htm.push('<td>'+'<button id="add_servergroup" class="btn btn-small btn-success">添加组权限</button>'+'</td>');
        htm.push('</tr>');
        htm.push('<tr>');
        htm.push('<td></td>');
        htm.push('<td></td>');
        htm.push('<td></td>');
        htm.push('</tr>');

        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td>'+'<input type="text" readonly="true" class="form-control"  value="'+username+'">'+'</td>');
            htm.push('<td>'+'<input type="text" readonly="true" class="form-control"  value="'+data[i][0]+'">'+'</td>');
            htm.push('<td>'+'<input type="text" readonly="true" class="form-control"  value="'+data[i][1]+'">'+'</td>');
            htm.push('<td>'+'<button id="delete_servergroup" username="'+username+'" servergroup="'+data[i][0]+'" class="btn btn-small btn-danger">删除组权限</button>'+'</td>');
            htm.push('</tr>');
        }

        htm.push('<tr>');
        htm.push('<td>'+'<button id="delete_user" username="'+username+'" class="btn btn-small btn-danger">删除用户</button>'+'</td>');
        htm.push('</tr>');

        htm.push('</table>');
        $('#update_user').html(htm.join(''));
    })
}


function servergroup_list_all(){
    $.getJSON('/group_list_all', function(data){
        var htm=['<select class="form-control" id="add_server_group">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#usergroupnamediv').html(htm.join(''));
    })
};

function project_info(p){
    var status = $('#project_div').attr('status')
    if (status == 'close') {
        var param = {
            project: p
        }
        $.getJSON('/project_info', param, function(data){
            var htm=['<table class="table table-hover">'];

            htm.push('<tr>');
            htm.push('<td width="120" align="right">Business line:</td>');
            htm.push('<td>'+data[0]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">environment:</td>');
            htm.push('<td>'+data[1]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">project:</td>');
            htm.push('<td>'+data[2]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">type:</td>');
            htm.push('<td>'+data[3]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">port:</td>');
            htm.push('<td>'+data[4]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">git:</td>');
            htm.push('<td>'+data[5]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">branch:</td>');
            htm.push('<td>'+data[6]+'</td>');
            htm.push('</tr>');

            htm.push('</table>');
            $('#project_div').html(htm.join(''));
        });
        $('#project_div').attr('status','open')
    }else{
        $('#project_div').html("");
        $('#project_div').attr('status','close')
    }
};


function config_info(p){
    var status = $('#config_div').attr('status')
    if (status == 'close') {
        var param = {
            project: p
        }
        $.getJSON('/config_info', param, function(data){
            var htm=['<table class="table table-hover">'];
            htm.push('<tr>');
            htm.push('<td colspan="2">'+'ip = $ip$'+'</td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td colspan="2">'+'numprocs = $pnum$'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[0][0]+':</td>');
            htm.push('<td><textarea id="'+data[0][0]+'" rows="5" cols="100"  readonly="readonly" >'+data[0][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[1][0]+':</td>');
            htm.push('<td><textarea id="'+data[1][0]+'" rows="5" cols="100"  readonly="readonly" >'+data[1][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[2][0]+':</td>');
            htm.push('<td><textarea id="'+data[2][0]+'" rows="5" cols="100"  readonly="readonly" >'+data[2][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[3][0]+':</td>');
            htm.push('<td><textarea id="'+data[3][0]+'" rows="5" cols="100"  readonly="readonly" >'+data[3][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[4][0]+':</td>');
            htm.push('<td><textarea id="'+data[4][0]+'" rows="5" cols="100"  readonly="readonly" >'+data[4][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[5][0]+':</td>');
            htm.push('<td><textarea id="'+data[5][0]+'" rows="5" cols="100"  readonly="readonly" >'+data[5][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[6][0]+':</td>');
            htm.push('<td>'+data[6][1]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[7][0]+':</td>');
            htm.push('<td>'+data[7][1]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[8][0]+':</td>');
            htm.push('<td>'+data[8][1]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[9][0]+':</td>');
            htm.push('<td>'+data[9][1]+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[10][0]+':</td>');
            htm.push('<td>'+data[10][1]+'</td>');
            htm.push('</tr>');

            htm.push('</table>');
            $('#config_div').html(htm.join(''));
        });
        $('#config_div').attr('status','open')
    }else{
        $('#config_div').html("");
        $('#config_div').attr('status','close')
    }
};


function host_list_table(p){
    var param={ project:p};
    $.getJSON('/hostlist', param,  function(data){
        var htm=['<table class="table table-hover">'];
        if (data!='' && data!=undefined && data!=null){
            if($('#leftDiv').attr('path') == "online"){
                htm.push('<thead><tr><th>hostname</th><th>ip</th><th>pnum</th><th>status</th><th>checkTime</th><th>commitID</th><th>Tag</th><th>stop</th></thead>');
                for(var i=0,len=data.length; i<len; i++){
                    if(data[i][1] != "essExpansion"){
                        htm.push('<tr>');
                        if (p.indexOf("online")!=0){
                            htm.push('<td>'+'<input type="checkbox" name="onlinehost" value="'+data[i][0]+'" checked="checked">'+data[i][1]+'</td>');
                        } else {
                            htm.push('<td>'+'<input type="checkbox" name="onlinehost" value="'+data[i][0]+'" >'+data[i][1]+'</td>');
                        }
                        htm.push('<td>'+data[i][0]+'</td>');
                        if (data[0][3]=='python' || data[0][3]=='nodejs'){
                            htm.push('<td>'+data[i][4]+'</td>');
                        }
                        if(data[i][6] == "RUNNING"){
                            htm.push('<td><div id="status'+data[i][0].replace(/\./g,"-")+'" class="sidebar-menu"><font color="Lime">'+data[i][6]+'</font></div></td>');
                        } else if(data[i][6] == "SSHOK"){
                            htm.push('<td><div id="status'+data[i][0].replace(/\./g,"-")+'" class="sidebar-menu"><font color="#FF9900">'+data[i][6]+'</font></div></td>');
                        } else {
                            htm.push('<td><div id="status'+data[i][0].replace(/\./g,"-")+'" class="sidebar-menu"><font color="red">'+data[i][6]+'</font></div></td>');
                        }
                        htm.push('<td><div id="checkTime'+data[i][0].replace(/\./g,"-")+'" class="sidebar-menu">'+data[i][7]+'</div></td>');
                        htm.push('<td><div id="commitID'+data[i][0].replace(/\./g,"-")+'" class="sidebar-menu">'+data[i][8]+'</div></td>');
                        htm.push('<td><div id="Tag'+data[i][0].replace(/\./g,"-")+'" class="sidebar-menu">'+data[i][10]+'</div></td>');
                        htm.push('<td>'+'<a href="javascript:;" onclick=stop_submit("'+data[i][0]+'");>stop</a>'+'</td>');
                        htm.push('</tr>');
                    }
                }
            }

            if($('#leftDiv').attr('path') == "project_admin"){
                htm.push('<thead><tr><th>hostname</th><th>ip</th><th>pnum</th><th>ENV</th><th>status</th><th>DeployConf</th><th>save</th><th>delete</th></tr></thead>');
                for(var i=0,len=data.length; i<len; i++){
                    if(data[i][1] != "essExpansion"){
                        htm.push('<tr>');
                        htm.push('<td>'+'<input type="text" class="form-control" id="hostname'+i+'" placeholder="hostname" value="'+data[i][1]+'">'+'</td>');
                        htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="hostip'+i+'" placeholder="data[i][0]" value="'+data[i][0]+'">'+'</td>');
                        htm.push('<td>'+'<input type="text" class="form-control" id="pnum'+i+'" placeholder="pnum" value="'+data[i][4]+'">'+'</td>');
                        htm.push('<td>'+'<input type="text" class="form-control" id="env'+i+'" placeholder="a=1,b=2" value="'+data[i][5]+'">'+'</td>');
                        if(data[i][6] == "RUNNING"){
                            htm.push('<td>'+'<font color="Lime">'+data[i][6]+'</font>'+'</td>');
                        } else if(data[i][6] == "SSHOK"){
                            htm.push('<td>'+'<font color="#FF9900">'+data[i][6]+'</font>'+'</td>');
                        }else{
                            htm.push('<td>'+'<font color="red">'+data[i][6]+'</font>'+'</td>');
                        }
                        htm.push('<td><button id="deploy_config" host="'+data[i][0]+'" class="btn btn-sm btn-danger" project="'+p+'" >更新supervisor</button></td>');
                        htm.push('<td><button id="update_host" host="'+data[i][0]+'" i="'+i+'" class="btn btn-sm btn-danger" project="'+p+'" >保存</button></td>');
                        htm.push('<td><button id="del_host" host="'+data[i][0]+'" class="btn btn-sm btn-danger" project="'+p+'" >delete</button></td>');
                        htm.push('</tr>');
                    }
                }
            }
        }
        htm.push('</table>');
        $('#host').html(htm.join(''));
    });
};


function host_list_status(p){
    var param={ project:p};
    $.getJSON('/hostlist', param,  function(data){
        if (data!='' && data!=undefined && data!=null){
            for(var i=0,len=data.length; i<len; i++){
                if(data[i][6] == "RUNNING"){
                    $('#status'+data[i][0].replace(/\./g,"-")).html('<font color="Lime">'+data[i][6]+'</font>');
                } else if(data[i][6] == "SSHOK"){
                    $('#status'+data[i][0].replace(/\./g,"-")).html('<font color="#FF9900">'+data[i][6]+'</font>');
                } else {
                    $('#status'+data[i][0].replace(/\./g,"-")).html('<font color="red">'+data[i][6]+'</font>');
                }
                $('#checkTime'+data[i][0].replace(/\./g,"-")).html(data[i][7]);
                $('#commitID'+data[i][0].replace(/\./g,"-")).html(data[i][8]);
                $('#Tag'+data[i][0].replace(/\./g,"-")).html(data[i][10]);
            }

        }
    });

};


function push_edit_host_table(p){
    var param={ project:p};
    $.getJSON('/hostlist', param,  function(data){
        var htm=['<table class="table table-hover">'];

        if($('#leftDiv').attr('path') == "project_admin"){
            htm.push('<thead><tr><th>hostname</th><th>ip</th><th>pnum</th><th>project</th></tr></thead>');
            $.each(data, function(ip, data){
                if(data[0] != "essExpansion"){
                    htm.push('<tr>');
                    htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="hostname" value="'+data[0]+'">'+'</td>');
                    htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_git" placeholder="ip" value="'+ip+'">'+'</td>');
                    htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="pnum" value="'+data[1]+'">'+'</td>');
                    htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_git" placeholder="project" value="'+data[2]+'">'+'</td>');
                    htm.push('</tr>');
                }
            })
            htm.push('<tr><td><button id="edit_host" class="btn btn-small btn-danger" project="'+p+'" >更新主机信息</button></td></tr>');
        }
        htm.push('</table>');
        $('#add_host_table').html(htm.join(''));

    });
};


function parseQuery(searchStr) {
    var search = searchStr || location.search.slice(1)
    var searchObj = {}
    search.split('&').forEach(function(param) {
        var paramArr = param.split('=')
        var k = paramArr[0]
        var v = paramArr[1]
        searchObj[k] = v
    })
    return searchObj
}

function addQuery(href, key, value) {
    var hrefArr = href.split('?')
    var url = hrefArr[0]
    var search = hrefArr[1] || ''
    var newSearchArr = []
    search.split('&').forEach(function(param) {
        var paramArr = param.split('=')
        var k = paramArr[0]
        if(k !== key) {
            newSearchArr.push(param)
        }
    })
    newSearchArr.push(key + '=' + value)
    return url + '?' + newSearchArr.filter(s => s !== '').join('&')
}


$("body").on('click', '.host_list', function(){
    var p = $(this).attr('data-project')
    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'project', p)
        $v.attr('href', newHref)
    })
    host_list_push(p)
});

function host_list_argv(p){

    host_list_push(avgr['project'])
}

function host_list_push(p){

    $('p').css('background','');
    $($('[data-project="'+p+'"]').find('p')[0]).css({"backgroundColor":"#C1FFC1"});

    host_list_table(p)
    online_tag(p)
    current_tag(p)

    var htm1=['<input type="hidden" name="project" id="ipt_project" value="'+p+'" />'];
    $('#select_project').html(htm1.join(''));

    var htm3=['<a href="javascript:;" class="project_info_table" status="close" onclick=\'project_info("'+p+'");\'>项目信息:    '+p+'</a>'];
    $('#project_button').html(htm3.join(''));

    var htm4=['<a href="javascript:;" class="config_info_table" status="close" onclick=\'config_info("'+p+'");\'>配置信息:    '+p+'</a>'];
    $('#config_button').html(htm4.join(''));

    if(p.split("_",1) == "online"){
        var htm5=['<button id="btn_submit" class="btn btn-warning" type="button">'+p.split("_",1)+'更新</button>'];
    }else{
        var htm5=['<button id="btn_submit" class="btn btn-success" type="button">'+p.split("_",1)+'更新</button>'];
    }

    $('#updatebutton').html(htm5.join(''));

    $('#ProgressBarDiv').html('');
    $('#cnt').html("");
    $('#resDiv').html("");
    $('#add_host_table').html("");
    $('#project_div').html("");
    $('#project_div').attr('status','close');
    $('#config_div').html("");
    $('#config_div').attr('status','close');

    clearInterval(timeout);

    if(timeout1){clearInterval(timeout1)};
        timeout1 = setInterval(function(){
            host_list_status(p);
    },10000);

}


$("body").on('click', '.host_list_admin', function(){
    $('p').css('background','');
    $($(this).find('p')[0]).css({"backgroundColor":"#C1FFC1"});

    var p = $(this).attr('data-project')

    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'project', p)
        $v.attr('href', newHref)
    })

    host_list_table(p)

    var htm1=['<input type="hidden" name="project" id="ipt_project" value="'+p+'" />'];
    $('#select_project').html(htm1.join(''));

    $('#ProgressBarDiv').html('');
    $('#cnt').html("");
    $('#resDiv').html("");
    $('#add_host_table').html("");
    $('#project_div').html("");
    $('#project_div').attr('status','close');
    $('#config_div').html("");
    $('#config_div').attr('status','close');
    project_button_div();
    config_button_div();
    push_add_host_table(p)
});


function selectAll(n){
    var a = document.getElementsByName(n);
    if(typeof(a[0]) != 'undefined'){
        if(a[0].checked){
            for(var i=0; i<a.length; i++){
                if (a[i].name == n) a[i].checked = false;
            }
        }else{
            for(var i=0; i<a.length; i++){
                if (a[i].name == n) a[i].checked = true;
            }
        }
    }
}


function next(i, hostLen){
    var param={ taskid:i };
    $.getJSON('/cmdreturns', param,  function(data){
        var percentage=parseInt(data.length * 100 / (hostLen+1));
        if(percentage<10){
            var percentage=10;
        }

        var ProgressBar='<div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';

        var ProgressBarDanger='<div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';

        $('#ProgressBarDiv').html(ProgressBar);

        if(data.length == hostLen+1){
            clearInterval(timeout);
        }

        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>主机</th><th>状态</th><th>执行过程</th></tr>');
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            if(data[i][2] == 'ok' ){
               htm.push('<td class="success">'+data[i][0]+'</td>');
               htm.push('<td class="success">'+data[i][2]+'</td>');
            }else{
               htm.push('<td class="danger">'+data[i][0]+'</td>');
               htm.push('<td class="danger">'+data[i][2]+'</td>');
               $('#ProgressBarDiv').html(ProgressBarDanger);
               clearInterval(timeout);
            }
            htm.push('<td><textarea rows="30" cols="80" readonly="readonly">'+data[i][3]+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#cnt').html(htm.join(''));
    });
};

function hostlisterrweb(){

    $.getJSON('/hostlisterr', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>project_name</th><th>hostname</th><th>ip</th><th>status</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#statistics').html(htm.join(''));
    });
};

function postlist(){

    $.getJSON('/port_list', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>port</th><th>project</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('</tr>');
        }
        $('#statistics').html(htm.join(''));
    });
};

function projectall(){

    $.getJSON('/project_list', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>group</th><th>project</th><th>port</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            //htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td><a href="/online?group='+data[i][0]+'&project='+data[i][1]+'" target="_blank">'+data[i][1]+'</a></td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('</tr>');
        }
        $('#statistics').html(htm.join(''));
    });
};

function online_log_time(p){
    var param={ project:p };
    $.getJSON('/online_log_time', param, function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>time</th><th>operation</th><th>taskid</th><th>tag</th><th>project</th><th>output</th><th>user</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+'<a href="javascript:;" onclick="online_log_info(\''+data[i][1]+'\');">'+DataTime+'</a>'+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#online_log_time').html(htm.join(''));
        $('#online_log').html("");

    });
};


$("body").on('click', '.online_log_time', function(){
    $('p').css('background','');
    $($(this).find('p')[0]).css({"backgroundColor":"#C1FFC1"});

    var p = $(this).attr('data-project')

    $('.presentationLink').each(function(k, v) {
        var $v = $(v)
        var href = $v.attr('href')
        var newHref = addQuery(href, 'project', p)
        $v.attr('href', newHref)
    })

    var param={ project:p };
    $.getJSON('/online_log_time', param, function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>time</th><th>operation</th><th>taskid</th><th>tag</th><th>project</th><th>output</th><th>user</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+'<a href="javascript:;" onclick="online_log_info(\''+data[i][1]+'\');">'+DataTime+'</a>'+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#online_log_time').html(htm.join(''));
        $('#online_log').html("");

    });
});

function online_log_all(){

    $.getJSON('/online_log_all', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>time</th><th>operation</th><th>taskid</th><th>tag</th><th>project</th><th>output</th><th>user</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+'<a href="javascript:;" onclick="online_log_info(\''+data[i][1]+'\');">'+DataTime+'</a>'+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('</tr>');
        }
        $('#online_log_time').html(htm.join(''));
        $('#online_log').html("");

    });
};

function online_log_info(id){
    var param={ taskid:id };
    $.getJSON('/cmdreturns', param,  function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>主机</th><th>状态</th><th>执行过程</th></tr>');
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            if(data[i][2] == 'ok' ){
               htm.push('<td class="success">'+data[i][0]+'</td>');
               htm.push('<td class="success">'+data[i][2]+'</td>');
            }else{
               htm.push('<td class="danger">'+data[i][0]+'</td>');
               htm.push('<td class="danger">'+data[i][2]+'</td>');
            }
            htm.push('<td><textarea rows="30" cols="80" readonly="readonly">'+data[i][3]+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#online_log').html(htm.join(''));
    });
};


//function getLocalTime(nS) {
//    return new Date(parseInt(nS) * 1000 ).toLocaleString()
//}


function add0(m){return m<10?'0'+m:m }


function getLocalTime(nS) {
    var date=new Date(parseInt(nS)* 1000);
    var year=date.getFullYear();
    var mon = date.getMonth()+1;
    var day = date.getDate();
    var hours = date.getHours();
    var minu = date.getMinutes();
    var sec = date.getSeconds();

    return year+'-'+add0(mon)+'-'+add0(day)+' '+add0(hours)+':'+add0(minu)+':'+add0(sec);
}



function project_button_div(){
    $('#project_button').html('<button id="open_add_project_edit" status="close" type="button" class="btn btn-small btn-info">编辑项目</button>');
};


function config_button_div(){
    $('#config_button').html('<button id="open_add_config_edit" status="close" type="button" class="btn btn-small btn-info">编辑配置</button>');
};

$("body").on('click', '#open_add_config_edit', function(){
    var  p = $('#ipt_project').val()
    if (p != undefined){
        push_edit_config_table(p);
    }
    else{
        alert('project_name null');
    };
});

$("body").on('click', '#open_add_project_edit', function(){
    var  p = $('#ipt_project').val()
    if (p != undefined){
        push_edit_project_table(p);
    }
    else{
        alert('project_name null');
    };
});


function push_edit_project_table(p){
    var status = $('#project_div').attr('status')
    if (status == 'close') {
        var param = {
            project: p
        }
        $.getJSON('/project_info', param, function(data){
            var htm=['<table class="table table-hover ">'];

            htm.push('<tr>');
            htm.push('<td width="120" align="right">Business line:</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="add_business" placeholder="" value="'+data[0]+'">'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">environment:</td>');
            htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_environment" placeholder="hockey" value="'+data[1]+'">'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">project:</td>');
            htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_nproject" placeholder="api" value="'+data[2]+'">'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">type:</td>');
            htm.push('<td>'+'<input type="text" readOnly="true" class="form-control" id="add_type" placeholder="python" value="'+data[3]+'">'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">port:</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="add_port" placeholder="go port[8000-10000]  python port[3000-5000]" value="'+data[4]+'">'+'</td>');
            htm.push('</tr>');


            htm.push('<tr>');
            htm.push('<td width="120" align="right">git:</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="add_git" placeholder="git://github.com/sre/op.git" value="'+data[5]+'">'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">branch:</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="add_branch" placeholder="python" value="'+data[6]+'">'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td></td>');
            htm.push('<td><div><div style="float:left"><button id="update_project" class="btn btn-small btn-success" >确认保存</button></div><div style="float:right"><button id="del_project" class="btn btn-small btn-danger">删除项目及关联的主机</button></div></div></td>');
            htm.push('</tr>');

            htm.push('</table>');
            $('#project_div').html(htm.join(''));
        });
        $('#project_div').attr('status','open')
    }else{
        $('#project_div').html("");
        $('#project_div').attr('status','close')
    }
};


$("#rmlock").on('click', function(){
    var  p = $('#ipt_project').val();
    if (p != undefined){
        var param = {
            project: p
        };

        $.getJSON('/rmpkl', param, function(data){
            alert(p + ' lock clear done!');
        });
    }
    else{
        alert('project_name null');
    };
});

$("#killtask").on('click', function(){
    var  p = $('#ipt_project').val();
    if (p != undefined){
        var param = {
            project: p
        };
        if (confirm('警告:请确认终止当前任务 '+ p +'?')) {
            $.getJSON('/killtask', param, function(data){
                alert('kill task ' + p + ' ' + data.status + ':' + data.log);
            });
        };
    }
    else{
        alert('project_name null');
    };
});

$("body").on('click', '#clean_git_cache', function(){
    var  p = $('#ipt_project').val();
    if (p != undefined){
        var param = {
            project: p
        };

        $.getJSON('/clean_git_cache', param, function(data){
            alert(p + ' git cache clear done!' + data);
        });
    }
    else{
        alert('project_name null');
    };
});


function push_edit_config_table(p){
    var status = $('#config_div').attr('status')
    if (status == 'close') {
        var param = {
            project: p
        }
        $.getJSON('/config_info', param, function(data){
            var htm=['<table class="table table-hover">'];

            htm.push('<tr>');
            htm.push('<td colspan="2">'+'ip = $ip$'+'</td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td colspan="2">'+'numprocs = $pnum$'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[0][0]+':</td>');
            htm.push('<td><textarea id="'+data[0][0]+'" rows="5" cols="100"  >'+data[0][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[1][0]+':</td>');
            htm.push('<td><textarea id="'+data[1][0]+'" rows="5" cols="100"  >'+data[1][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[2][0]+':</td>');
            htm.push('<td><textarea id="'+data[2][0]+'" rows="5" cols="100"  >'+data[2][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[3][0]+':</td>');
            htm.push('<td><textarea id="'+data[3][0]+'" rows="5" cols="100"  >'+data[3][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[4][0]+':</td>');
            htm.push('<td><textarea id="'+data[4][0]+'" rows="5" cols="100"  >'+data[4][1]+'</textarea></td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[5][0]+':</td>');
            htm.push('<td><textarea id="'+data[5][0]+'" rows="5" cols="100"  >'+data[5][1]+'</textarea></td>');
            htm.push('</tr>');


            if (data[6][1]=="yes"){
                htm.push('<tr>');
                htm.push('<td width="120" align="right">'+data[6][0]+':</td>');
                htm.push('<td>'+'<select class="form-control" id="'+data[6][0]+'"><option value="yes" selected = "selected">yes</option><option value="no">no</option></select>'+'</td>');
                htm.push('</tr>');
            }else{
                htm.push('<tr>');
                htm.push('<td width="120" align="right">'+data[6][0]+':</td>');
                htm.push('<td>'+'<select class="form-control" id="'+data[6][0]+'"><option value="yes">yes</option><option value="no" selected = "selected">no</option></select>'+'</td>');
                htm.push('</tr>');
            }

            if (data[7][1]=="yes"){
                htm.push('<tr>');
                htm.push('<td width="120" align="right">'+data[7][0]+':</td>');
                htm.push('<td>'+'<select class="form-control" id="'+data[7][0]+'"><option value="yes" selected = "selected">yes</option><option value="no">no</option></select>'+'</td>');
                htm.push('</tr>');
            }else{
                htm.push('<tr>');
                htm.push('<td width="120" align="right">'+data[7][0]+':</td>');
                htm.push('<td>'+'<select class="form-control" id="'+data[7][0]+'"><option value="yes">yes</option><option value="no" selected = "selected">no</option></select>'+'</td>');
                htm.push('</tr>');
            }


            if (data[8][1]=="yes"){
                htm.push('<tr>');
                htm.push('<td width="120" align="right">'+data[8][0]+':</td>');
                htm.push('<td>'+'<select class="form-control" id="'+data[8][0]+'"><option value="yes" selected = "selected">yes</option><option value="no">no</option></select>'+'</td>');
                htm.push('</tr>');
            }else{
                htm.push('<tr>');
                htm.push('<td width="120" align="right">'+data[8][0]+':</td>');
                htm.push('<td>'+'<select class="form-control" id="'+data[8][0]+'"><option value="yes">yes</option><option value="no" selected = "selected">no</option></select>'+'</td>');
                htm.push('</tr>');
            }

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[9][0]+':</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="'+data[9][0]+'" placeholder="/" value="'+data[9][1]+'">'+'</td>');
            htm.push('</tr>');

            htm.push('<tr>');
            htm.push('<td width="120" align="right">'+data[10][0]+':</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="'+data[10][0]+'" placeholder="200" value="'+data[10][1]+'">'+'</td>');
            htm.push('</tr>');


            htm.push('<tr>');
            htm.push('<td></td>');
            htm.push('<td><button id="update_config" class="btn btn-small btn-success" >确认保存</button></td>');
            htm.push('</tr>');
            htm.push('</table>');
            $('#config_div').html(htm.join(''));
        });
        $('#config_div').attr('status','open')
    }else{
        $('#config_div').html("");
        $('#config_div').attr('status','close')
    }
};


function online_tag(p){
    var param = {
        project: p
    }
    $.getJSON('/online_tag', param, function(data){
        var htm=['<select id="select_tag" class="form-control">'];
        if(data.length == 0){
            htm.push('<option value="null">null update</option>');
        }
        else{
            for(var i=0,len=data.length; i<len; i++){
                htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
            }
        }
        htm.push('</select>');
        $('#tag_div').html(htm.join(''));
    });
};


function current_tag(p){
    var param = {
        project: p
    }
    $.getJSON('/current_tag', param, function(data){
        $('#online_tag_div').html(data[0]);
    });
};




$("#lastlog").on('click', function(){
    var  p = $('#ipt_project').val()
    if (p == undefined){
        alert('project_name null');
    }
    var param={ project:p };
    $.getJSON('/lock_check', param, function(lockdata){
        if(lockdata['status'] == "ok"){
            var percentage=100;
        }else{
            var percentage=50;
        }
        var ProgressBar='<div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';
        var ProgressBarDanger='<div class="progress-bar progress-bar-danger progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';

        $.getJSON('/lastlog', param,  function(data){
            var htm=['<table class="table table-bordered">'];
            htm.push('<tr><th>主机</th><th>状态</th><th>执行过程</th></tr>');
            var status=''
            for(var i=0,len=data.length; i<len; i++){
                htm.push('<tr>');
                if(data[i][2] == 'fail' ){
                   var status=data[i][2]
                   htm.push('<td class="danger">'+data[i][0]+'</td>');
                   htm.push('<td class="danger">'+data[i][2]+'</td>');
                   clearInterval(timeout);
                }else{
                   htm.push('<td class="success">'+data[i][0]+'</td>');
                   htm.push('<td class="success">'+data[i][2]+'</td>');
                }
                htm.push('<td><textarea rows="30" cols="80" readonly="readonly">'+data[i][3]+'</textarea></td>');
                htm.push('</tr>');
            }
            htm.push('</table>');
            if(status == 'fail'){
                $('#ProgressBarDiv').html(ProgressBarDanger);
                //clearInterval(timeout);
                alert('严重警告：注意看错误，上线失败了！！！')
            } else {
                $('#ProgressBarDiv').html(ProgressBar);
            }
            $('#cnt').html(htm.join(''));
        });
    });
});


$("body").on('click', '#update_config', function(){
    if (confirm('请确认配置信息')) {

        var project    = $('#ipt_project').val()
        var make       = $('#make').val()
        var supervisor = $('#supervisor').val()
        var config     = $('#config').val()
        var remarks    = $('#remarks').val()
        var startcmd   = $('#startcmd').val()
        var packfile   = $('#packfile').val()
        var istag      = $('#istag').val()
        var checkport  = $('#checkport').val()
        var checkhttp  = $('#checkhttp').val()
        var httpurl    = $('#httpurl').val()
        var httpcode   = $('#httpcode').val()

        if(!project ){
            alert('project null');
            return false;
        }

        var param = {
            project     : project,
            make        : make,
            supervisor  : supervisor,
            config      : config,
            remarks     : remarks,
            startcmd    : startcmd,
            packfile    : packfile,
            istag       : istag,
            checkport   : checkport,
            checkhttp   : checkhttp,
            httpurl     : httpurl,
            httpcode    : httpcode
        }

        $.post('/update_config', param, function(data){
            alert(data.status+"  "+data.log);
            if(data.status == 'ok'){
                $('#config_div').html("");
                $('#config_div').attr('status','close')
                project_list();
            }
        }, 'json');
    };
});


function online_statistics(){
    $.getJSON('/online_statistics', function(data){
        var htm=['<table class="table table-hover" border="2">'];


        htm.push('<tr><td rowspan="2"><h5>project</h5></td><td colspan="3"><h5>前1周</h5></td><td colspan="3"><h5>前2周</h5></td><td colspan="3"><h5>前3周</h5></td><td colspan="3"><h5>前4周</h5></td></tr>');

        htm.push('<tr><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td><td><h5>update</h5></td><td><h5>restart</h5></td><td><h5>fallback</h5></td></tr>');

        $.each(data, function(i, h){
            htm.push('<tr>');
            htm.push('<td>'+i+'</td>');
            htm.push('<td>'+h[0]+'</td>');
            htm.push('<td>'+h[1]+'</td>');
            htm.push('<td>'+h[2]+'</td>');
            htm.push('<td>'+h[3]+'</td>');
            htm.push('<td>'+h[4]+'</td>');
            htm.push('<td>'+h[5]+'</td>');
            htm.push('<td>'+h[6]+'</td>');
            htm.push('<td>'+h[7]+'</td>');
            htm.push('<td>'+h[8]+'</td>');
            htm.push('<td>'+h[9]+'</td>');
            htm.push('<td>'+h[10]+'</td>');
            htm.push('<td>'+h[11]+'</td>');
            htm.push('</tr>');

        })

        htm.push('</table>');
        $('#statistics').html(htm.join(''));
    })
};

function cmslog(){
    $.getJSON('/cmslog', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr><td><h5>@timestamp</h5></td><td><h5>auth_name</h5></td><td><h5>method</h5></td><td><h5>status</h5></td><td><h5>request_api</h5></td><td><h5>remote_addr</h5></td><td><h5>request_time</h5></td></tr>');
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            for(var u=0,len1=data[i].length; u<len1; u++){
                if(u==0){
                    var DataTime = getLocalTime(data[i][0])
                    htm.push('<td>'+DataTime+'</td>');
                }else{
                    htm.push('<td>'+data[i][u]+'</td>');
                }
            }
            htm.push('</tr>');
        }

        htm.push('</table>');
        $('#cms_log').html(htm.join(''));
    })
};


function erplog(){
    $.getJSON('/erplog', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr><td><h5>@timestamp</h5></td><td><h5>auth_name</h5></td><td><h5>method</h5></td><td><h5>status</h5></td><td><h5>request_api</h5></td><td><h5>parameter</h5></td><td><h5>description</h5></td><td><h5>error_message</h5></td><td><h5>platform</h5></td></tr>');
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<tr>');
            for(var u=0,len1=data[i].length; u<len1; u++){
                if(u==0){
                    var DataTime = getLocalTime(data[i][0])
                    htm.push('<td>'+DataTime+'</td>');
                }else{
                    htm.push('<td>'+data[i][u]+'</td>');
                }
            }
            htm.push('</tr>');
        }

        htm.push('</table>');
        $('#erp_log').html(htm.join(''));
    })
};


function stop_submit(ip){
    var p = $('#ipt_project').val()
    if (p != undefined){
        if (confirm('请确认停止服务'+ p +'!')) {
            var param = {
                operation: 'serviceStop',
                project: p,
                client: ip,
            };
            updateonline(param)
        };
    }
    else{
        alert('project_name null');
    };
};


function stopserver(param){

    $.post('/stopserver', param, function(data){
        $("#resDiv").html( "&nbsp;&nbsp;&nbsp;&nbsp;operation:&nbsp;&nbsp;"+data.operation+"<br>&nbsp;&nbsp;&nbsp;&nbsp;taskid:&nbsp;&nbsp;"+data.taskid+"<br>&nbsp;&nbsp;&nbsp;&nbsp;logout:&nbsp;&nbsp;"+data.output+"<br>&nbsp;&nbsp;&nbsp;&nbsp;hostlist:&nbsp;&nbsp;"+data.host+"<br>&nbsp;&nbsp;&nbsp;&nbsp;tag:&nbsp;&nbsp;"+data.tag+"<br>&nbsp;&nbsp;&nbsp;&nbsp;project:&nbsp;&nbsp;"+data.project);
        if(timeout){clearInterval(timeout)};
        timeout = setInterval(function(){
            next(data.taskid, 1);
        },4000);
        $('#cnt').html("");
    }, 'json');
};


function workorder_group_list(){
    $.getJSON('/group_list', function(data){
        var htm=['<select class="form-control" id="selectgroup" onchange="workorder_project_list()">'];
        for(var i=0,len=data.length; i<len; i++){
            htm.push('<option value="'+data[i]+'">'+data[i]+'</option>');
        }
        htm.push('</select>');
        $('#group').html(htm.join(''));
        workorder_project_list();
    })
};


function workorder_project_list(){

    var selectgroup = $('#selectgroup').val()
    var param = {
        group: selectgroup,
        functype: 'workorder'
    }

    $.getJSON('/project', param , function(data){
        var htm=['<select class="form-control" id="selectproject">'];
        $.each(data, function(g, projectlist){
            var h=projectlist.sort();
            for(var i=0,len=h.length; i<len; i++){
                if(h[i].indexOf("online_")>-1){
                    htm.push('<option value="'+h[i]+'">'+h[i]+'</option>');
                }
            }
        })
        htm.push('</select>');
        $('#project').html(htm.join(''));
    });
};


$("body").on('click', '.workordermenu', function(){
    var menu = $(this).attr('menu');
    //userservicegrouplist(username)
    selectworkmenu(menu)
});


function selectworkmenu(menu){
    if(menu == 'createworkorder'){
        createworkorder()
        workorder_group_list()

    } else if(menu == 'waitworkorder'){
        waitworkorder()
    } else if(menu == 'doneworkorder'){
        doneworkorder()
    }
};

function createworkorder(){
    var htm=['<table class="table table-hover" border="2">'];
    htm.push('<tr>');
    htm.push('<td>group:</td>');
    htm.push('<td><div id="group"></div></td>');
    htm.push('</tr>');
    htm.push('<tr>');
    htm.push('<td>project:</td>');
    htm.push('<td><div id="project"></div></td>');
    htm.push('</tr>');
    htm.push('<tr>');
    htm.push('<td>remarks:</td>');
    htm.push('<td><textarea id="remarks" rows="5" cols="100"></textarea></td>');
    htm.push('</tr>');
    htm.push('<tr>');
    htm.push('<td></td>');
    htm.push('<td><button id="subworkorder" class="btn btn-small btn-success">提交工单</button></td>');
    htm.push('</tr>');
    htm.push('</table>');

    $('#workorder_div').html(htm.join(''));
}
function waitworkorder(){
    $.getJSON('/wait_workorder', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr>');
        htm.push('<td>组</td>');
        htm.push('<td>项目</td>');
        htm.push('<td>申请人</td>');
        htm.push('<td>申请时间</td>');
        htm.push('<td>状态</td>');
        //htm.push('<td>执行人</td>');
        //htm.push('<td>完成时间</td>');
        htm.push('<td>关闭工单</td>');
        htm.push('<td>备注</td>');
        htm.push('</tr>');

        for(var i=0,len=data.length; i<len; i++){
            var applicationtime = getLocalTime(data[i][3])
            //var completiontime = getLocalTime(data[i][6])
            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td><a href="/online?group='+data[i][0]+'&project='+data[i][1]+'" target="_blank">'+data[i][1]+'</a></td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+applicationtime+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            //htm.push('<td>'+data[i][5]+'</td>');
            //htm.push('<td>'+data[i][6]+'</td>');
            htm.push('<td><button id="downworkorder" time="'+data[i][3]+'" class="btn btn-small btn-success">关闭工单</button></td>');
            htm.push('<td><textarea id="remarks" rows="3" cols="40">'+data[i][7]+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#workorder_div').html(htm.join(''));
    })

}
function doneworkorder(){
    $.getJSON('/done_workorder', function(data){
        var htm=['<table class="table table-hover" border="2">'];
        htm.push('<tr>');
        htm.push('<td>组</td>');
        htm.push('<td>项目</td>');
        htm.push('<td>申请人</td>');
        htm.push('<td>申请时间</td>');
        htm.push('<td>状态</td>');
        htm.push('<td>执行人</td>');
        htm.push('<td>完成时间</td>');
        htm.push('<td>备注</td>');
        htm.push('</tr>');
        for(var i=0,len=data.length; i<len; i++){
            var applicationtime = getLocalTime(data[i][3])
            var completiontime = getLocalTime(data[i][6])

            htm.push('<tr>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][2]+'</td>');
            htm.push('<td>'+applicationtime+'</td>');
            htm.push('<td>'+data[i][4]+'</td>');
            htm.push('<td>'+data[i][5]+'</td>');
            htm.push('<td>'+completiontime+'</td>');
            htm.push('<td><textarea id="remarks" rows="2" cols="25">'+data[i][7]+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');
        $('#workorder_div').html(htm.join(''));
    })
}


$("body").on('click', '#subworkorder', function(){
    if (confirm('请确认提交工单信息')) {
        var group   = $('#selectgroup').val()
        var project = $('#selectproject').val()
        var remarks = $('#remarks').val()
        if (project != undefined){
            var param = {
                group:    group,
                project:  project,
                remarks:  remarks,
            };
            $.post('/add_workorder', param, function(data){
                alert(data.status+"  "+data.log);
            }, 'json');
        }
        else{
            alert('workorder project name null');
        };
    }
});




$("body").on('click', '#downworkorder', function(){
    var applicationtime = $(this).attr('time')
    if (confirm('请确认关闭工单')) {
        var param = {
            applicationtime: applicationtime
        }
        $.post('/update_workorder', param, function(data){
            alert(data.status+"  "+data.log);
            waitworkorder();

        }, 'json');
    };
});




$("body").on('click', '.statistics', function(){
    var menu = $(this).attr('menu');
    if(menu == 'portlist'){
        postlist()
    } else if(menu == 'projectlist'){
        projectall()
    } else if(menu == 'hostlisterr'){
        hostlisterrweb()
    } else if(menu == 'onlinenum'){
        online_statistics()
    }
});

$("body").on('click', '.hostmanage', function(){
    $('#create_hosts_result').html("");
    $('#ProgressBarDiv').html("");
    var menu = $(this).attr('menu');
    if(menu == 'createhost'){
        createhost()
    } else if(menu == 'hostmanagelist'){
        hostmanagelist()
    } 
});


function createhost(){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>创建主机</th><th>选择</th><th>备注</th></tr>');
            htm.push('<tr>');
            htm.push('<td>业务线</td>');
            htm.push('<td>'+'<select class="form-control" id="selectbigbusiness" onchange="get_area()"><option value="pp-online">皮皮线上</option><option value="pp-test">皮皮测试</option><option value="zy-online">最右线上</option><option value="zy-test">最右测试</option><option value="hanabi-online">火花线上</option><option value="hanabi-test">火花测试</option></select>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>可用区</td>');
            htm.push('<td>'+'<div id="area" class="sidebar-menu"> </div>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>配置</td>');
            htm.push('<td>'+'<div id="configuration" class="sidebar-menu"> </div>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>镜像</td>');
            htm.push('<td>'+'<select class="form-control" id="selectimage"><option value="centos7-zy1">centos7-zy1</option><option value="centos7-db1">centos7-db1</option><option value="centos7-ffmpeg">centos7-ffmpeg</option></select>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td>主机名</td>');
            htm.push('<td>'+'<input type="text" class="form-control" id="hostnames" placeholder="多台主机,空格分割主机名" value="">'+'</td>');
            htm.push('<td>多台空格分割</td>');
            htm.push('</tr>');
            htm.push('<tr>');
            htm.push('<td></td>');
            htm.push('<td>'+'<button id="create_hosts" class="btn btn-small btn-success" >创建主机实例</button>'+'</td>');
            htm.push('<td></td>');
            htm.push('</tr>');
        $('#hostmanage').html(htm.join(''));

    get_area()
};

function hostmanagelist(){

    $.getJSON('/hostlistall', function(data){
        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>hostname</th><th>ip</th><th>实例id</th><th>配置</th><th>重新初始化</th><th>修改主机名</th><th>关机注销</th></tr>');

        for(var i=0,len=data.length; i<len; i++){
            var DataTime = getLocalTime(data[i][1])

            htm.push('<tr>');
            htm.push('<td>'+data[i][1]+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][0]+'</td>');
            htm.push('<td>'+data[i][3]+'</td>');
            htm.push('<td>'+'重新初始化'+'</td>');
            htm.push('<td>'+'修改主机名'+'</td>');
            htm.push('<td>'+'关机注销'+'</td>');
            htm.push('</tr>');
        }
        $('#hostmanage').html(htm.join(''));
    });
};

function get_area(){
    var selectbigbusiness = $('#selectbigbusiness').val()
    var param = {
        bigbusiness: selectbigbusiness
    }
    $.getJSON('/get_area', param , function(data){

        var htm=['<select class="form-control" id="selectarea" onchange="get_configuration()">'];

        $.each(data, function(value, valuename){
            htm.push('<option value="'+value+'">'+valuename+'</option>');
        })
        htm.push('</select>');
        $('#area').html(htm.join(''));
        get_configuration()
    });
}


function get_configuration(){
    var selectarea = $('#selectarea').val()
    var param = {
        area: selectarea
    }
    $.getJSON('/get_configuration', param , function(data){

        var htm=['<select class="form-control" id="selectconfiguration">'];
        $.each(data, function(value, valuename){
            htm.push('<option value="'+value+'">'+valuename+'</option>');
        })
        htm.push('</select>');

        $('#configuration').html(htm.join(''));
    });
}


$("body").on('click', '#create_hosts', function(){
    $('#create_hosts_result').html("");
    $('#ProgressBarDiv').html("");
    var bigbusiness   = $('#selectbigbusiness').val()
    var area   = $('#selectarea').val()
    var configuration   = $('#selectconfiguration').val()
    var image   = $('#selectimage').val()
    var hostnames   = $('#hostnames').val()

    if (confirm('请确认创建主机')) {
        var param = {
            bigbusiness: bigbusiness,
            area: area,
            configuration: configuration,
            image: image,
            hostnames: hostnames,
        }
        $.post('/create_hosts', param, function(data){
            alert(data.status+"  "+data.log);
            if(data.status == 'ok'){
                if(timeout2){clearInterval(timeout2)};
                timeout2 = setInterval(function(){
                    get_create_hosts_result(data.create_hosts_taskid);
                },2000);
                //$('#create_hosts_result').html("");
                //$('#ProgressBarDiv').html("");
            } else {
                alert(data.status + ' 失败 ' + data.log)
            };
        }, 'json');
    };
});



function get_create_hosts_result(create_hosts_taskid){
    var param={ taskid: create_hosts_taskid };
    $.getJSON('/get_create_hosts_result', param,  function(data){

        var htm=['<table class="table table-bordered">'];
        htm.push('<tr><th>主机</th><th>任务id</th><th>状态</th><th>执行过程</th></tr>');
        if(data.status == 'ok'){
            var percentage=100;
            var ProgressBarStatus='progress-bar-success';
            clearInterval(timeout2);
            htm.push('<tr>');
            htm.push('<td class="success">'+data.hostnames+'</td>');
            htm.push('<td class="success">'+data.taskid+'</td>');
            htm.push('<td class="success">'+data.status+'</td>');
            htm.push('<td><textarea rows="30" cols="80" readonly="readonly">'+data.log+'</textarea></td>');
            htm.push('</tr>');
        }  else if(data.status == 'wait') {
            var percentage=50;
            var ProgressBarStatus='progress-bar-success';
        } else if(data.status == 'fail') {
            var percentage=60;
            var ProgressBarStatus='progress-bar-danger';
            clearInterval(timeout2);
            htm.push('<tr>');
            htm.push('<td class="danger">'+data.hostnames+'</td>');
            htm.push('<td class="danger">'+data.taskid+'</td>');
            htm.push('<td class="danger">'+data.status+'</td>');
            htm.push('<td><textarea rows="30" cols="80" readonly="readonly">'+data.log+'</textarea></td>');
            htm.push('</tr>');
        }
        htm.push('</table>');

        $('#create_hosts_result').html(htm.join(''));

        var ProgressBar='<div class="progress-bar '+ProgressBarStatus+' progress-bar-striped" role="progressbar" aria-valuenow="'+percentage+'" aria-valuemin="0" aria-valuemax="100" style="width: '+percentage+'%">'+percentage+'%</div>';
        $('#ProgressBarDiv').html(ProgressBar);

    });
};
