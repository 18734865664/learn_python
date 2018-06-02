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

exitFlag = 0
return_info = {}



def test(request):
    # return HttpResponse(u'hello')
    return render(request, 'build_jenkins/index.html')

class jenkinsBuildJobThread(threading.Thread):

    def __init__(self, timestamp, job_name_queue):
        threading.Thread.__init__(self)
        self.timestamp = timestamp
        self.job_name_queue = job_name_queue
    def run(self):
       build_job(self.job_name_queue, self.timestamp)


       

        
 

@csrf_exempt
def build(request):
    # 初始化job_args表
    obj = updateMysql()
    obj.create_job_args_table()
    lock = threading.Lock()

    # 接收request请求
    if request.method == "GET":
        return HttpResponseRedirect("/build_jenkins/") 
    
    elif request.method == "POST":
        jenkins_obj_name = request.POST['jenkins_obj_name']
        timestamp = request.POST['timestamp']
        # 从数据库中查询套餐对应应用列表
        db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
        cursor = db.cursor() 
        sql = 'select jenkins_obj_member from jenkins_info.jenkins_obj where jenkins_obj_name = \"{}\"'.format(jenkins_obj_name)
        cursor.execute(sql)
        jenkins_build_list_tmp = cursor.fetchall()[0][0]
        db.commit()
        db.close()
        try:
            jenkins_build_list = jenkins_build_list_tmp.split(',')
        except:
            jenkins_build_list = jenkins_build_list_tmp.split() 
        build_job_name_queue = queue.Queue(len(jenkins_build_list))
        import pdb; pdb.set_trace()
        threads = []
        # 创建线程池
        for thread_id in range(1,4):
            thread = jenkinsBuildJobThread(timestamp, build_job_name_queue)
            thread.start()
            threads.append(thread)
            
        # 填充队列
        lock.acquire()
        for build_job_name in jenkins_build_list:
            build_job_name_queue.put(build_job_name)
        lock.release()
            
            
        while not build_job_name_queue.empty():
            pass
   
        exitFlag = 1
        for t in threads:
            t.join()

        return_json = json.dumps(return_info) 
        return HttpResponse(return_json, content_type="application/json")


def build_job(job_name_queue, timestamp):

    """
        接收一个jenkins的job列表，和一个时间戳。
        执行具体的构建触发动作，并返回查询服务的id

    """
    while not exitFlag:
        if not job_name_queue.empty():
            build_job_name = job_name_queue.get()
            db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
            cursor = db.cursor() 
            sql_build_args = "select * from jenkins_info.job_args where job_name = \"{}\"".format(build_job_name.replace('-', '_'))
            cursor.execute(sql_build_args)
            build_args = list(cursor.fetchall()[0])
            db.commit()
            db.close()
            url = settings.JENKINS_URL + build_args[0] + "/buildWithParameters"     
            data = {
                "branch_parents": build_args[2],
                "ftp_path": build_args[3],
                "mvn_args": build_args[4],
                "subitems": build_args[5],
                "laster_build_num": build_args[6]
            }
            # 初始化参数表后，默认ftp_path是当天的目录，如果传入参数中上线时间不为空，则替换该参数
            if timestamp:
                data["ftp_path"] = data["ftp_path"].split("_v0.0_")[0] + str(timestamp)

            return_info[build_job_name] = build_args[6]
            # data = urllib.parse.urlencode(data).encode('utf-8')
            data_tmp = ''
            for i in data.keys():
                if data_tmp:
                    data_tmp = data_tmp + '&' + i + '=' + str(data[i])
                else:
                    data_tmp = data_tmp + i + '=' + str(data[i])
            print("hello")
            subprocess.call(["curl -X  POST http://jenkins:jenkins@10.100.140.161:8080/job/{}/buildWithParameters -d \"{}\"".format(build_job_name, data_tmp)], shell=True)
            while True:
                db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
                cursor = db.cursor() 
                sql_build_args = "select count(*) from jenkins_info.job_result where job_name = \"{}\", and build_id = {}".format(build_job_name.replace('-', '_'), int(data["laster_build_num"]))
                cursor.execute(sql_build_args)
                build_count = int(cursor.fetchall()[0][0])
                db.commit()
                db.close()
                if build_count > 0:
                    break
                else:
                    time.sleep(1)
        else:
            pass
        time.sleep(1)
 
