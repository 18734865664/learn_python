# coding:utf-8
import os
import sys
import commands
import time
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect ,HttpResponse ,StreamingHttpResponse
from django.shortcuts import render
import json

reload(sys)
sys.setdefaultencoding('utf-8')
from .form import CmsConfigForms,DeliverConfigForms,EditConfigForms
from .models import CmsConfig ,DeliverConfigHistory,VersionOfConfig
import  tasks.tasks as task

# Create your views here.

@login_required(login_url='/accounts/login/')
def cms_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        form = CmsConfigForms()
        cms_config_parameter = CmsConfig.objects.all()
        return render(request,'cms/cms_config.html',locals())
    elif request.method == 'POST':
        form = CmsConfigForms(request.POST)
        #if form.is_valid():
        cms_config_name = request.POST['cms_config_name']
        app_name = request.POST['app_name']
        software_name = request.POST['software_name']
        config_file_name = request.POST['config_file_name']
        deliver_host = ','.join(request.POST.getlist('deliver_host'))
        #CmsConfig.objects.update_or_create()
        if CmsConfig.objects.filter(cms_config_name=cms_config_name):
            CmsConfig.objects.filter(cms_config_name=cms_config_name).update(app_name=app_name,software_name=software_name,config_file_name=config_file_name,deliver_host=deliver_host,config_content='')
        else:
            CmsConfig(cms_config_name=cms_config_name,app_name=app_name,software_name=software_name,config_file_name=config_file_name,deliver_host=deliver_host,config_content='').save()
        #else:
        return HttpResponseRedirect("/cms/cms_config")
        #return render(request,'cms/cms_config.html',locals())


@login_required(login_url='/accounts/login/')
def del_cms_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        cms_config_name = request.GET['cms_config_name']
        CmsConfig.objects.filter(cms_config_name=cms_config_name).delete()

    return HttpResponseRedirect("/cms/cms_config")


@login_required(login_url='/accounts/login/')
def get_cms_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    cms_config_id = request.GET['cms_config_id']
    config_file_name = CmsConfig.objects.get(id = cms_config_id).config_file_name
    cms_config_obj = open(config_file_name)
    try:
        config_content = cms_config_obj.read()
    finally:
        cms_config_obj.close()
    return HttpResponse(config_content,content_type='text')


@login_required(login_url='/accounts/login/')
def save_cms_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    cms_config_id = request.POST['cms_config_id']
    config_content = request.POST['config_content']
    config_file_name = CmsConfig.objects.get(id = cms_config_id).config_file_name
    CmsConfig.objects.filter(id =  cms_config_id).update(config_content=config_content)
    cms_config_obj = open(config_file_name,"w")
    cms_config_obj.write(config_content)
    cms_config_obj.close()
    return HttpResponse("成功")

@login_required(login_url='/accounts/login/')
def deliver_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        form = DeliverConfigForms()
        cms_config_parameter = CmsConfig.objects.all()
        return render(request,'cms/deliver_config.html',locals())
    elif request.method == "POST":
        form = DeliverConfigForms(request.POST)
        config_file_id = request.POST['select_file_name'].split(',')[0]
        cms_config_id = VersionOfConfig.objects.get(id = config_file_id).cms_config_id
        app_name = CmsConfig.objects.get(id = cms_config_id).app_name
        opt_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        backup_file_path = VersionOfConfig.objects.get(id = config_file_id).backup_file_path
        backup_file_name = VersionOfConfig.objects.get(id = config_file_id).backup_file_name
        software_name = CmsConfig.objects.get(id = cms_config_id).software_name
        deliver_host = ','.join(request.POST.getlist('deliver_host_list'))
        whether_to_reload = request.POST['whether_to_reload']
        addressee_list = ','.join(request.POST.getlist('addressee_list'))
        copy_list = ','.join(request.POST.getlist('copy_list'))
        file_name = os.path.basename(request.POST['config_file_name']).split('.conf')[0]
        os.system('cp -rf ' + backup_file_path + '/' + backup_file_name + "/* /data/ngx_openresty/nginx/conf/")
        history_content = {}
        for i in deliver_host.split(','):
            history_content_tmp = task.deliver_cms_config(file_name,software_name,i,whether_to_reload)
            history_content[i] = history_content_tmp
        history_content_str = str(history_content)
        history_content_reObj = re.findall(r'[\'\"]result[\'\"]: false',history_content_str,re.M|re.I)
        false_num = len(history_content_reObj)
        DeliverConfigHistory.objects.get_or_create(username=request.user.username,deliver_host=deliver_host,history_content=json.dumps(history_content),whether_to_reload=whether_to_reload,opt_time=opt_time,config_file_id = config_file_id,false_num = false_num)
        #return HttpResponse(json.dumps(history_content),content_type="application/json")
        return HttpResponseRedirect('/histrecord/deliverconfig/')

@login_required(login_url='/accounts/login/')
def get_other_parameter(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    #version = request.GET['version']
    cms_config_id = request.GET['cms_config_id']
    other_parameter = CmsConfig.objects.filter(id=cms_config_id).values_list('app_name','software_name','config_file_name','deliver_host','id')
    other_parameter_list = []
    for i in other_parameter:
        other_parameter_dict = {}
        other_parameter_dict['app_name'] = i[0]
        other_parameter_dict['software_name'] = i[1]
        other_parameter_dict['config_file_name'] = i[2]
        other_parameter_dict['deliver_host'] = i[3]
        other_parameter_dict['id'] = i[4]
        other_parameter_list.append(other_parameter_dict)
    return HttpResponse(json.dumps(other_parameter_list),content_type="application/json")


@login_required(login_url='/accounts/login/')
def get_backup_other_parameter(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    #version = request.GET['version']
    backup_file_id = request.GET['backup_file_id']
    cms_config_id = VersionOfConfig.objects.get(id = backup_file_id).cms_config_id
    reasons_for_change = VersionOfConfig.objects.get(id = backup_file_id).reasons_for_change
    other_parameter = CmsConfig.objects.filter(id=cms_config_id).values_list('app_name','software_name','config_file_name','deliver_host','id')
    other_parameter_list = []
    for i in other_parameter:
        other_parameter_dict = {}
        other_parameter_dict['app_name'] = i[0]
        other_parameter_dict['software_name'] = i[1]
        other_parameter_dict['config_file_name'] = i[2]
        other_parameter_dict['deliver_host'] = i[3]
        other_parameter_dict['id'] = i[4]
        other_parameter_dict['reasons_for_change'] = reasons_for_change
        other_parameter_list.append(other_parameter_dict)
    return HttpResponse(json.dumps(other_parameter_list),content_type="application/json")



@login_required(login_url='/accounts/login/')
def edit_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        form = EditConfigForms()
        cms_config_parameter = CmsConfig.objects.all()
        return render(request,'cms/edit_config.html',locals())
    elif request.method == 'POST':
        form = EditConfigForms(request.POST,request.FILES)
        config_file = request.FILES['config_file']
        config_file_name = request.POST['config_file_name']
        with open(os.path.dirname(config_file_name) + '/' + config_file.name, 'wb+') as upload_file:
            for chunk in config_file.chunks(chunk_size=1024):
                upload_file.write(chunk)
        return HttpResponseRedirect('cms_edit')


@login_required(login_url='/accounts/login/')
def download_file(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        form = EditConfigForms()
        def read_file(config_file_name,chunk_size=512):
            with open(config_file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        config_file_name = request.GET['config_file_name']
        file_name = os.path.basename(config_file_name)
        response=StreamingHttpResponse(read_file(config_file_name))
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename="{0}"'.format(file_name)
        return response

@login_required(login_url='/accounts/login/')
def checking_cms_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    form = EditConfigForms()
    cms_config_id = request.GET['cms_config_id']
    app_name = CmsConfig.objects.get(id = cms_config_id).app_name
    file_name = os.path.basename(CmsConfig.objects.get(id = cms_config_id).config_file_name).split('.conf')[0]
    software_name = CmsConfig.objects.get(id = cms_config_id).software_name
    deliver_host = CmsConfig.objects.get(id = cms_config_id).deliver_host
    checking_cms_config = {}

    for i in deliver_host.split(','):
        checking_cms_config_tmp = task.checking_cms_config(software_name,file_name,i)
        checking_cms_config[i] = checking_cms_config_tmp
    json_data = json.dumps(checking_cms_config)
    return HttpResponse(json_data,content_type="application/json")


@login_required(login_url='/accounts/login/')
def get_file_name(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    cms_config_id = request.GET['cms_config_id']
    file_name_list = list(VersionOfConfig.objects.filter(cms_config_id = cms_config_id).order_by('-id')[:10].values_list('backup_file_path','backup_file_name','reasons_for_change','id'))
    return HttpResponse(json.dumps(file_name_list),content_type='application/json')


@login_required(login_url='/accounts/login/')
def save_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level

    cms_config_id = request.GET['cms_config_id']
    reasons_for_change = request.GET['reasons_for_change']
    app_name = CmsConfig.objects.get(id = cms_config_id).app_name
    software_name = CmsConfig.objects.get(id=cms_config_id).software_name
    backup_file_name = commands.getoutput("sh /data/shell/deliver_" + software_name + "_config.sh " + app_name + "|grep 'BACKUP_FILE_NAME='|awk -F 'BACKUP_FILE_NAME=' '{print $2}'")
    backup_file_path = '/data/backup/' + app_name + '/' + software_name + '/'
    VersionOfConfig.objects.get_or_create(cms_config_id =  cms_config_id,reasons_for_change =reasons_for_change,backup_file_name = backup_file_name,backup_file_path= backup_file_path)
    return HttpResponse(json.dumps([{'backup_file_name':backup_file_name}]),content_type ="application/json")

