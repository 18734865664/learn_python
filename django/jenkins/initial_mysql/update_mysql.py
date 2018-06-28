#! /usr/local/python3.4.4/bin/python3
# encodig: utf-8

import pymysql
import sys
import os
sys.path.insert(0, os.getcwd())
from .get_file_list import  getFileList
from .get_args import getJenkinsArgs

'''
接收到一个job_name，更新mysql库中job_args表中对应记录
'''


class updateMysql():
    def __init__(self, job_name):
        self.mysql_host = "10.100.140.161"
        self.mysql_user = "jenkins"
        self.mysql_pass = "jenkins"
        self.mysql_port = "3306"
        self.mysql_dbname = "jenkins_info"
        self.job_name = job_name
    
    # job参数表，更新数据，单条数据
    def update_single_job_args(self):
        
        db = pymysql.connect(host = self.mysql_host, user = self.mysql_user, passwd = self.mysql_pass, port = int(self.mysql_port))
        cursor = db.cursor() 
        sql_query_row_name = "select job_name_row from jenkins_info.job_args where job_name = \"{}\";".format(self.job_name)
        # print(sql_query_row_name)
        cursor.execute(sql_query_row_name)
        try:
            job_name_row = cursor.fetchall()[0][0]
        except:
            job_name_row = self.job_name
        job_workspace_file = '/app/jenkins/jobs/' + job_name_row
        job_config_file = job_workspace_file + "/config.xml"
        obj = getJenkinsArgs(job_config_file, job_name_row)
        f = open(job_workspace_file + "/nextBuildNumber", 'r')
        build_num = f.readline()
        sql_build_update = "update jenkins_info.job_args set laster_build_num={} where job_name = \"{}\";".format(build_num, self.job_name)
        # print(sql_build_update)
        cursor.execute(sql_build_update)
        db.commit()
        db.close()


if __name__ == "__main__":
    obj = updateMysql("ceshi_pip2")
    obj.create_job_args_table()
        
