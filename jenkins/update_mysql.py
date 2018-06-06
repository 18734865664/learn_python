#! /usr/local/python3/bin/python3
# encodig: utf-8

import pymysql
import sys
sys.path.insert(0, '/data/nfs/python/learn_python/jenkins/')
from get_file_list import  getFileList
from get_args import getJenkinsArgs
import get_args

class update_mysql():
    def __init__(self):
        self.mysql_host = "10.100.137.179"
        self.mysql_user = "root"
        self.mysql_pass = "123123"
        self.mysql_port = "3306"
        self.mysql_dbname = "jenkins_info"

    def create_job_args_table(self):
        # 实例化mysql
        db = pymysql.connect(host = self.mysql_host, user = self.mysql_user, passwd = self.mysql_pass, port = int(self.mysql_port))
        
        # 创建游标对象
        cursor = db.cursor() 
        
        # 如果不存在就建库jenkins_info
        try:
            sql = "create database if not exists {};".format((self.mysql_dbname))
            cursor.execute(sql)
        except:
            print("库已存在")
        # 如果表不存在，则创建表
        sql1 = "create table if not exists jenkins_info.{}( \
              `job_name` VARCHAR(100) NOT NULL, \
              `job_name_row` VARCHAR(100) NOT NULL, \
              `branch_parents` VARCHAR(1000) NOT NULL DEFAULT 'NULL', \
              `ftp_path` VARCHAR(100) NOT NULL DEFAULT 'NULL', \
              `mvn_args`VARCHAR(50) NOT NULL DEFAULT '\[\"prod\"\]', \
              `subitems_name` VARCHAR(200) NOT NULL DEFAULT 'NULL'  \
              );".format(("job_args"))
        cursor.execute(sql1)

        # 获取job列表
        job_name_file_obj = getFileList("/data/nfs/jenkins/jobs/").get_file_list()
        
        # 获取参数列表
        for job_name in job_name_file_obj:
            job_workspace_file = '/data/nfs/jenkins/jobs/' + job_name
            job_config_file = job_workspace_file + "/config.xml"
            obj = getJenkinsArgs(job_config_file, job_name)
        
 

if __name__ == "__main__":
    obj = update_mysql()
    obj.create_job_args_table()
        
