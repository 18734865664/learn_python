from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.http import HttpResponseRedirect ,HttpResponse ,StreamingHttpResponse
import subprocess
from initial_mysql.update_mysql import updateMysql
import pymysql
from django.views.decorators.csrf import csrf_exempt 
import urllib.parse
import urllib.request
import json
import queue
import threading
import time
from celery import Celery
from .tasks import build as tasks_build

@csrf_exempt
def build(request):
    # 接收request请求
    if request.method == "GET":
        return HttpResponseRedirect("/build_jenkins/") 
    
    elif request.method == "POST":
        # print("收到post请求")
        jenkins_obj = request.POST['jenkins_obj']
        # timestamp = request.POST['timestamp']
        data = json.loads(jenkins_obj)
        obj = updateMysql()
        obj.create_job_args_table()
        tasks_build.delay(data)
        # print(len(data["jenkins_obj_name"]))
        return HttpResponse("test")
