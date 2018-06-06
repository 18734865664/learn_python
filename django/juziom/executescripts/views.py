# -*- coding:utf-8 -*-
import json
import os
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, RequestContext

from configspec.models import Execute_script_config, Code_updates_config
from tasks.tasks import execute_scripts
from .form import ExeScriptForms

reload(sys)
sys.setdefaultencoding('utf-8')


@login_required()
def get_script_list(request, cnfid, script_type):
    script_list = []
    script_list1 = []
    cnfid = request.GET.get('cnfid')
    script_type = request.GET.get('script_type')
    configs = Code_updates_config.objects.filter(id=cnfid)
    shell = Execute_script_config.objects.all()
    if script_type == 'php':
        for i in configs:
            c = {}
            d = []
            try:
                f_list = os.listdir(i.sync_path + 'script/')
            except:
                c['script_file'] = 'False'
            else:
                for s in f_list:
                    if os.path.splitext(s)[1] == '.php':
                        d.append(s)
            c['sync_path'] = i.sync_path
            c['target_host'] = i.target_host
            c['script_file'] = ','.join(d)
            script_list.append(c)
        return HttpResponse(json.dumps(script_list), content_type='application/json')
    else:
        c = {}
        e = {}
        for s in shell:
            e['excute_program'] = s.execute_program
            e['script_name'] = s.script_name
            e['script_path'] = s.script_path
            script_list1.append(e)
        for i in configs:
            c['target_host'] = i.target_host
            script_list.append(c)
        return HttpResponse(json.dumps(script_list + script_list1), content_type='application/json')


@login_required()
def common_commands(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    username = request.user.username
    if request.method == 'GET':
        form = ExeScriptForms()

        project_from_sql = Code_updates_config.objects.all().values('id', 'project_name')
        execute_script_config = Execute_script_config.objects.all()
        return render(request, 'executescripts/commoncommands.html', locals(), context_instance=RequestContext(request))
    elif request.method == 'POST':
        script_file = request.POST['script-file']
        execute_param = request.POST['execute_param']
        target_host = ','.join(request.POST.getlist('target_host'))
        script_type = request.POST['script_type']
        script_type = request.POST['script_type']
        Action = [u'执行脚本', script_file + " " + execute_param]
        if script_type == 'php':
            execute_scripts.delay(execute_program='/data/php/bin/php', script_file=script_file + ' ' + execute_param,
                                  target_host=target_host,
                                  username=username)
            return render(request, 'jump/jumpe.html', locals())


        else:
            execute_scripts.delay(execute_program='/bin/bash', script_file=script_file + ' ' + execute_param,
                                  target_host=target_host, username=username)
            return render(request, 'jump/jumpe.html', locals())
