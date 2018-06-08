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
from celery import Celery, task



return_info = {}
global exitFlag
exitFlag = {}


# 线程池，继承threading.Thread, 用于向后端发送请求
class jenkinsBuildJobThread(threading.Thread):

    def __init__(self, timestamp, job_name_queue, jenkins_obj_name):
        threading.Thread.__init__(self)
        self.timestamp = timestamp
        self.job_name_queue = job_name_queue
        self.jenkins_obj_name = jenkins_obj_name
    # 重写run方法，线程启动时调用
    def run(self):
       build_job(self.job_name_queue, self.timestamp, self.jenkins_obj_name)
 
# 线程池，继承threading.Thread, 用于接收请求
class jenkinsJobThread(threading.Thread):

    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
    # 重写run方法，线程启动时调用
    def run(self):
        series_thread(self.q)

@task
# @csrf_exempt
def build(data):
    # jenkins_obj = data.POST['jenkins_obj']
    # data = json.loads(jenkins_obj)
    lock_test = threading.Lock()
    # 从数据库中查询套餐对应应用列表
    # db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
    # cursor = db.cursor() 
    # sql = 'select jenkins_obj_member from jenkins_info.jenkins_obj where jenkins_obj_name = \"{}\"'.format(data["jenkins_obj_name"])
    # cursor.execute(sql)
    # jenkins_build_list_tmp = cursor.fetchall()[0][0]
    # db.commit()
    # db.close()
    # import pdb; pdb.set_trace()
    exitFlag[data["jenkins_obj_name"][0]] = len(data["jenkins_obj_name"])
    
    # 创建队列
    build_job_name_queue = queue.Queue(len(data["jenkins_obj_name"]))
    threads = []

    # 创建线程池
    for thread_id in range(1,4):
        thread = jenkinsBuildJobThread(data["timestamp"], build_job_name_queue, data["jenkins_obj_name"][0])
        thread.start()
        threads.append(thread)
    return_info[data["jenkins_obj_name"][0]] = {}
        
    # 填充队列
    lock_test.acquire()
    for build_job_name in data["jenkins_obj_name"]:
        build_job_name_queue.put(build_job_name)
    lock_test.release()
        
    # 如果队列不为空，阻塞
    while not build_job_name_queue.empty():
        time.sleep(1)
        pass
   
    # exitFlag是一个全局参数，声明，作为退出标识
    # global exitFlag;

    # 阻塞至进程停止
    for t in threads:
        t.join()

    return_json = json.dumps(return_info[data["jenkins_obj_name"][0]]) 
    # return HttpResponse(return_json, content_type="application/json")
    subprocess.call(["curl -X POST http://10.100.137.179:8000/jenkins/build/celery -d 'return_data=\"{}\"'".format(return_json)], shell=True)
        

def build_job(job_name_queue, timestamp, jenkins_obj_name):

    """
        接收一个jenkins的job列表，和一个时间戳。
        执行具体的构建触发动作，并返回查询服务的id

    """
    lock_test = threading.Lock()
    while True:
        lock_test.acquire()
        # 监听工作队列
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
                "next_build_num": int(build_args[6]) + 1,
                "lock_job" : int(build_args[7])
            }

            # 用来阻塞同一job的并行请求
            while data["lock_job"] == 1:
                db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
                cursor = db.cursor() 
                sql_query_lock = "select * from jenkins_info.job_args where job_name = \"{}\"".format(build_job_name.replace('-', '_'))
                cursor.execute(sql_query_lock)
                build_args_tmp = list(cursor.fetchall()[0])
                data["lock_job"] = int(build_args_tmp[7])
                data["next_build_num"] = int(build_args_tmp[6]) + 1
                if build_args_tmp[7] == 0:
                    time.sleep(1)
                    sql_set_lock = "update jenkins_info.job_args set lock_job = 1, laster_build_num = \"{}\" where job_name = \"{}\"".format(str(int(data["next_build_num"])), build_job_name.replace('-', '_'))
                    db.commit()
                    db.close()
                    break
                db.commit()
                db.close()
                time.sleep(1)

            # 初始化参数表后，默认ftp_path是当天的目录，如果传入参数中上线时间不为空，则替换该参数
            if timestamp:
                data["ftp_path"] = data["ftp_path"].split("_v0.0_")[0] + "_v0.0_" + str(timestamp)
            return_info[jenkins_obj_name][build_job_name] = int(build_args[6]) + 1
            data_tmp = ''

            
            db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
            cursor = db.cursor() 
            sql_set_lock = "update jenkins_info.job_args set lock_job = 1, laster_build_num = \"{}\" where job_name = \"{}\";".format(str(int(data["next_build_num"])), build_job_name.replace('-', '_'))
            cursor.execute(sql_set_lock)
            db.commit()
            db.close()

            
            # 拼接触发job使用的参数列表
            for i in data.keys():
                if data_tmp:
                    data_tmp = data_tmp + '&' + i + '=' + str(data[i])
                else:
                    data_tmp = data_tmp + i + '=' + str(data[i])
            subprocess.call(["curl -X  POST http://jenkins:jenkins@10.100.140.161:8080/job/{}/buildWithParameters -d \"{}\"".format(build_job_name, data_tmp)], shell=True)

            # 阻塞，判断build是否完成
            while True:
                db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
                cursor = db.cursor() 
                sql_build_args = "select count(*) from jenkins_info.job_result where job_name_build_id = \"{}\";".format(build_job_name.replace('-', '_') + '-' + str(data["next_build_num"]))
                print(sql_build_args)
                cursor.execute(sql_build_args)
                build_count = int(cursor.fetchall()[0][0])
                db.commit()
                db.close()
                # print("exitFlag: " + str(exitFlag[jenkins_obj_name]))
                if build_count > 0:
                    break
                else:
                    time.sleep(1)
            exitFlag[jenkins_obj_name] = exitFlag[jenkins_obj_name] - 1
        if exitFlag[jenkins_obj_name] == 0:
            break
        time.sleep(1)
        print("world")
        lock_test.release()
 
