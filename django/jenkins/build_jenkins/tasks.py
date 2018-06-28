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
import crypt

'''
tasks.py作用：
1. 解析views接收到的套餐列表, 
2. 向后端jenkins发送构建请求, 异步执行
3. 套餐内任务全部执行后，回调接口
'''


return_info = {}
global exitFlag
exitFlag = {}


# 线程池，继承threading.Thread, 用于向celery发送任务
class jenkinsBuildJobThread(threading.Thread):

    def __init__(self, data, job_name_queue, jenkins_obj_tag):
        threading.Thread.__init__(self)
        self.data = data
        self.job_name_queue = job_name_queue
        self.jenkins_obj_tag = jenkins_obj_tag
    # 重写run方法，线程启动时调用
    def run(self):
       build_job(self.job_name_queue, self.data, self.jenkins_obj_tag)
 
# 线程池，继承threading.Thread, 用于接收请求
class jenkinsJobThread(threading.Thread):


    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
    # 重写run方法，线程启动时调用
    def run(self):
        series_thread(self.q)

@task
# 用于接收views中传入的请求
def build(data):
    '''
        接收到调用信息后，创建线程列表，下发具体任务，直到全部任务中止

    '''
    lock_test = threading.Lock()

    # 定义唯一性标识
    jenkins_obj_tag = crypt.crypt(str(data.keys()))

    # 用来指定退出job线程的标识
    exitFlag[jenkins_obj_tag] = len(data)
    
    # 创建任务队列
    build_job_name_queue = queue.Queue(len(data))
    threads = []
    
    # 创建线程池
    for thread_id in range(1,4):
        thread = jenkinsBuildJobThread(data, build_job_name_queue, jenkins_obj_tag)
        thread.start()
        threads.append(thread)
    return_info[jenkins_obj_tag] = {}
        
    # 填充任务队列
    lock_test.acquire()
    for build_job_name in data:
        build_job_name_queue.put(build_job_name)
    lock_test.release()
        
    # 如果队列不为空，阻塞进程，直到执行具体工作的函数消费完队列中的任务
    while not build_job_name_queue.empty():
        time.sleep(1)
        pass
   
    # 等待每一个派生进程全部停止
    for t in threads:
        t.join()

    return_json = json.dumps(return_info[jenkins_obj_tag]) 
    # return HttpResponse(return_json, content_type="application/json")
    # 构建结束后，回调
    subprocess.call(["curl -X POST http://10.100.140.161:8000/jenkins/build/celery -d 'return_data=\"{}\"'".format(return_json)], shell=True)
        

# 每次触发构建，会传入一个任务列表和时间戳，这里负责解析后，向服务器发送构建指令
def build_job(job_name_queue, data, jenkins_obj_tag):

    """
        接收一个jenkins的job列表，和一个时间戳。
        执行具体的构建触发动作，并返回查询服务的id

    """
    lock_test = threading.Lock()
    while True:
        lock_test.acquire()
        # 监听工作队列，队列未空，持续消费
        if not job_name_queue.empty():
            build_job_name = job_name_queue.get()    # 从队列中取出jenkins_job_name
            obj = updateMysql(build_job_name)        # 根据job_name 更新数据库得job_args信息
            obj.update_single_job_args()
            
            # 获取job_args 中记录属性值
            db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
            cursor = db.cursor() 
            sql_build_args = "select * from jenkins_info.job_args where job_name = \"{}\"".format(build_job_name)
            cursor.execute(sql_build_args)
            build_args = list(cursor.fetchall()[0])
            db.commit()
            db.close()
            url = settings.JENKINS_URL + build_args[0] + "/buildWithParameters"     
            base_data = {
                'job_name_row': build_args[1],
                "branch_parents": build_args[2],
                "ftp_path": build_args[3],
                "mvn_args": build_args[4].split(',')[0],
                "subitems": build_args[5],
                "next_build_num": int(build_args[6]),
                "lock_job" : int(build_args[7])
            }

            # 用来阻塞同一job的并行请求，该jenkins job已经有任务占用，数据库lock_job字段会置一
            while base_data["lock_job"] == 1:
                db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
                cursor = db.cursor() 
                sql_query_lock = "select * from jenkins_info.job_args where job_name = \"{}\"".format(build_job_name)
                cursor.execute(sql_query_lock)
                build_args_tmp = list(cursor.fetchall()[0])
                base_data["lock_job"] = int(build_args_tmp[7])
                base_data["next_build_num"] = int(build_args_tmp[6])
                if build_args_tmp[7] == 0:
                    time.sleep(1)
                    sql_set_lock = "update jenkins_info.job_args set lock_job = 1, laster_build_num = \"{}\" where job_name = \"{}\"".format(str(int(base_data["next_build_num"])), build_job_name)
                    db.commit()
                    db.close()
                    break
                db.commit()
                db.close()
                time.sleep(1)

            # 初始化参数表后，默认ftp_path是当天的目录，如果传入参数中上线时间不为空，则替换该参数
            if "timestamp" in data[build_job_name]:
                try:
                    time_tag = time.strftime('%w', time.strptime(data[build_job_name]["timestamp"], '%Y%m%d'))
                    base_data["ftp_path"] = base_data["ftp_path"].split("_")[0] + "_" + time_tag + "_" + str(data[build_job_name]["timestamp"])
                except:
                    print("传入时间格式有误")
                    break


            # 初始化参数表后，如果传入参数中branches_name不为空，则替换该参数
            if "branches_name" in data[build_job_name]:
                base_data["branch_parents"] = data[build_job_name]['branches_name']


            return_info[jenkins_obj_tag][build_job_name] = int(build_args[6])
            data_tmp = ''

            # 将数据库job_args中 lock_job置1
            db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
            cursor = db.cursor() 
            sql_set_lock = "update jenkins_info.job_args set lock_job = 1 where job_name = \"{}\";".format(build_job_name)
            cursor.execute(sql_set_lock)
            db.commit()
            db.close()

            
            # 拼接触发job使用的参数列表
            for i in base_data.keys():
                if data_tmp:
                    data_tmp = data_tmp + '&' + i + '=' + str(base_data[i])
                else:
                    data_tmp = data_tmp + i + '=' + str(base_data[i])

            # 像jenkins服务器发送构建请求
            curl_cmd = "curl -X  POST http://jenkins:jenkins@10.100.140.161:8080/job/{}/buildWithParameters -d \"{}\"".format(base_data["job_name_row"], data_tmp)
            print(curl_cmd)
            subprocess.call([curl_cmd], shell=True)

            # 阻塞，判断build是否完成，如果正常退出，会在数据库result表中插入一条记录
            while True:
           
                db = pymysql.connect(host = settings.MYSQL_HOST, user = settings.MYSQL_USER, passwd = settings.MYSQL_PASS, port = int(settings.MYSQL_PORT))
                cursor = db.cursor() 
                sql_build_args = "select count(*) from jenkins_info.job_result where job_name_build_id = \"{}\";".format(build_job_name + '-' + str(base_data["next_build_num"]))
                cursor.execute(sql_build_args)
                build_count = int(cursor.fetchall()[0][0])
                db.commit()
                db.close()
                print("查询")
                if build_count > 0:
                    break
                else:
                    time.sleep(1)
            exitFlag[jenkins_obj_tag] = exitFlag[jenkins_obj_tag] - 1
        if exitFlag[jenkins_obj_tag] == 0:
            break
        time.sleep(1)
        lock_test.release()
 
