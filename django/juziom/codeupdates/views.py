# -*- coding:utf-8 -*-
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from configspec.models import Code_updates_config
from libtools.git_commit import Commit_Log
from libtools.salt_api import *
from tasks.tasks import sync_code, rollback_code, sync_code_restart_service, rollback_code_restart_service, sendtomail
from .form import CodeUpForms, CodeRoForms

reload(sys)
sys.setdefaultencoding('utf-8')


@login_required()
def get_cnf_list(request, cnfid):
    oid_list = []
    cnfid = request.GET['cnfid']
    configs = Code_updates_config.objects.filter(id=cnfid)
    for i in configs:
        c = {}
        c['sync_path'] = i.sync_path
        c['sync_module'] = i.sync_module
        c['target_host'] = i.target_host
        c['exclude_parameter'] = i.exclude_parameter.exclude_parameter
        oid_list.append(c)
    return HttpResponse(json.dumps(oid_list), content_type='application/json')


@login_required()
def get_rollback_commit(request, sync_path):
    sync_path = request.GET['sync_path']
    full_commmit = Commit_Log(sync_path)
    return HttpResponse(json.dumps(full_commmit), content_type='application/json')

@login_required(login_url="/accounts/login/")
def code_updates(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    username = request.user.username
    if request.method == 'GET':
        form = CodeUpForms()
        return render(request, 'codeupdates/code_updates.html', locals())
    elif request.method == 'POST':
        form = CodeUpForms(request.POST)
        if form.is_valid():
            project_name = Code_updates_config.objects.get(id=request.POST['project_name']).project_name
            sync_path = request.POST['sync_path']
            sync_module = request.POST['sync_module']
            exclude_parameter = request.POST['exclude_parameter']
            change_content = request.POST['change_content']
            target_host = ','.join(request.POST.getlist('target_host'))
            restart_service = request.POST['restart_service']
            mailto = request.POST.get('mailto', '')
            cc = request.POST['mailcc']
            #            return HttpResponse(cc)
            if restart_service == 'no':
                jobid = sync_code.delay(project_name, sync_module, exclude_parameter, change_content, target_host,
                                        sync_path,
                                        username=username)
                sendtomail.delay(project_name, username, jobid, mailto, change_content, cc)
                Action = [project_name, u'上线']
                return render(request, 'jump/jump.html', locals())
            else:
                jobid = sync_code_restart_service.delay(project_name, sync_module, exclude_parameter, change_content,
                                                        target_host, sync_path,
                                                        username=username)
                sendtomail.delay(project_name, username, jobid, mailto, change_content, cc)
                Action = [project_name, u'上线']
                return render(request, 'jump/jump.html', locals())
        else:
            a = Code_updates_config.objects.all()
            return render(request, 'codeupdates/code_updates.html', locals())


@login_required(login_url="/accounts/login/")
def code_rollback(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    username = request.user.username
    if request.method == 'GET':
        form = CodeRoForms()
        a = Code_updates_config.objects.all()
        return render(request, 'codeupdates/code_rollback.html', locals())
    elif request.method == 'POST':
        form = CodeRoForms(request.POST)
        if form.is_valid():
            project_name = Code_updates_config.objects.get(id=request.POST['project_name']).project_name
            sync_path = request.POST['sync_path']
            sync_module = request.POST['sync_module']
            exclude_parameter = request.POST['exclude_parameter']
            change_content = request.POST['change_content']
            rollback_commit = request.POST['rollback_commit']
            target_host = ','.join(request.POST.getlist('target_host'))
            restart_service = request.POST['restart_service']
            mailto = request.POST.get('mailto', '')
            cc = request.POST['mailcc']
            if restart_service == 'no':
                jobid = rollback_code.delay(project_name, sync_module, exclude_parameter, change_content, target_host,
                                            sync_path,
                                            rollback_commit, username=username)
                sendtomail.delay(project_name, username, jobid, mailto, change_content, cc)
                Action = [project_name, u'回滚']
                return render(request, 'jump/jump.html', locals())
            else:
                jobid = rollback_code_restart_service.delay(project_name, sync_module, exclude_parameter,
                                                            change_content,
                                                            target_host, sync_path,
                                                            rollback_commit, username=username)
                sendtomail.delay(project_name, username, jobid, mailto, change_content, cc)
                Action = [project_name, u'回滚']
                return render(request, 'jump/jump.html', locals())
        else:
            a = Code_updates_config.objects.all()
            return render(request, 'codeupdates/code_updates.html', locals())
