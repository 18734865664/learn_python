# -*- coding:utf-8 -*-
import datetime
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, RequestContext

from configspec.models import Code_updates_config
from cms.models import DeliverConfigHistory,CmsConfig,VersionOfConfig
from libtools.salt_api import *
from .models import Sync_history, Exe_script_history

reload(sys)
sys.setdefaultencoding('utf-8')


@login_required()
def get_job_content(request, jobid):
    sapi = SaltAPI()
    jobid = request.GET['jobid']
    job_content = sapi.jobs_content(jobid)
    return HttpResponse(json.dumps(job_content), content_type='application/json')

@login_required()
def sync_history(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        sub = datetime.date.today().weekday()
        begintime = str(datetime.date.today() - datetime.timedelta(days=sub)) + " " + "00:00"
        endtime = str(datetime.date.today()) + " " + "23:59"
        data = Sync_history.objects.filter(date_time__range=(begintime, endtime))
        counts = len(data)
        obname = []
        dis = []
        sapi = SaltAPI()
        sync_history = Sync_history.objects.filter().order_by('-id')[:20]
        # return HttpResponse(sapi.jobs_list())
        for i in data:
            name = Code_updates_config.objects.get(project_name=i.project_name).project_name
            obname.append(name)
        fine = list(set(obname))
        for id_fine in fine:
            a = {}
            i_tems = obname.count(id_fine)
            a['names'] = id_fine
            a['countc'] = i_tems
            dis.append(a)
        return render(request, 'histrecord/operarecord.html', locals(),
                      context_instance=RequestContext(request))


@login_required()
def execute_history(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        sapi = SaltAPI()
        exe_history = Exe_script_history.objects.filter().order_by('-id')[:20]
        return render(request, 'histrecord/executerecord.html', locals(),
                      context_instance=RequestContext(request))


@login_required()
def deliver_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    deliver_config_history = []
    deliver_config_obj = DeliverConfigHistory.objects.filter().order_by('-id')
    for obj in  deliver_config_obj:
        deliver_config_history_tmp = {}
        deliver_config_history_tmp['id'] = obj.id
        deliver_config_history_tmp['cms_config_name'] =   CmsConfig.objects.get( id = VersionOfConfig.objects.get(id= obj.config_file_id).cms_config_id).cms_config_name
        deliver_config_history_tmp['reasons_for_change'] = VersionOfConfig.objects.get(id= obj.config_file_id).reasons_for_change
        deliver_config_history_tmp['deliver_host'] = obj.deliver_host
        deliver_config_history_tmp['username'] = obj.username
    #    deliver_config_history_tmp['history_content'] = obj.history_content
        deliver_config_history_tmp['whether_to_reload'] = obj.whether_to_reload
        deliver_config_history_tmp['opt_time'] = obj.opt_time
        deliver_config_history_tmp['false_num'] = obj.false_num
        deliver_config_history.append(deliver_config_history_tmp)

    return render(request, 'histrecord/deliverconfig.html', locals())

@login_required()
def get_deliver_content(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    deliver_id = request.GET['deliver_id']
    deliver_content = DeliverConfigHistory.objects.get(id=deliver_id).history_content
    return HttpResponse(deliver_content,content_type="application/json")
    
