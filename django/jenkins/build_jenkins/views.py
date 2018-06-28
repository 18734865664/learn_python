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


'''
接收到请求，调用tasks.py中函数，处理收到的参数列表
'''

@csrf_exempt
def build(request):
    # 接收request请求
    if request.method == "GET":
        return HttpResponseRedirect("/build_jenkins/") 
    
    elif request.method == "POST":
        # print("收到post请求")
        # 解析出请求中的参数json
        jenkins_obj = request.POST['jenkins_obj_list']
        data = json.loads(jenkins_obj)
        tasks_build.delay(data)
        return HttpResponse("test")
