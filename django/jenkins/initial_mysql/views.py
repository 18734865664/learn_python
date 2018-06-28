from django.shortcuts import render
from django.conf import settings
from initial_mysql.update_mysql import updateMysql
from django.http import HttpResponse
from initial_mysql.get_file_list import getFileList
# Create your views here.


'''
接收到请求，更新mysql中job_args全表

'''

def init(request):
    # 获取job列表
    job_name_file_obj = getFileList("/app/jenkins/jobs/").get_file_list()
    
    # 初始化
    for job_name_row in job_name_file_obj:
        print(job_name_row)
        obj = updateMysql(job_name_row)
        obj.update_single_job_args()
    return HttpResponse(u"初始化job_args表完成")

