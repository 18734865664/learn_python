from django.shortcuts import render
from django.conf import settings
from initial_mysql.update_mysql import updateMysql
from django.http import HttpResponse
# Create your views here.

def init(request):
    obj = updateMysql()
    obj.create_job_args_table()
    return HttpResponse(u"hello")

