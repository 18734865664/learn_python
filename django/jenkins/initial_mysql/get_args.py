#! /usr/local/python3.4.4/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180523

import xml.sax
import re
import time
import pymysql
import sys
import os
sys.path.insert(0, os.getcwd())
from .get_file_list import getFileList
import subprocess

""" 
getArgs: 
用来获取jenkins job配置文件，xml格式

"""

mysql_host = "10.100.140.161"
mysql_user = "jenkins"
mysql_pass = "jenkins"
mysql_port = "3306"
mysql_dbname = "jenkins_info"


class getArgs(xml.sax.ContentHandler):

    def __init__(self, job_name):
        self.current_data = ""
        self.name = []
        self.args = {}
        self.ftp_file_tag = ""
        self.time_tag = ""
        self.content = ""
        self.job_name = job_name
    

    # 遇到元素开始时执行
    def startElement(self, name, args):
        self.current_data = name
        if self.current_data == "script" and self.name == "ftp_path":
            self.content = ""
   
    # 遇到元素结束时执行
    def endElement(self, name):
        if name == "properties":
            if 'subitems_name' in self.args and self.args['subitems_name']:
                for subitems_name_tmp in self.args['subitems_name']:
                    # import pdb; pdb.set_trace()
                    f = open('/app/jenkins/jobs/' + self.job_name + '/nextBuildNumber')
                    build_num = f.readline()
                    db = pymysql.connect(host = mysql_host, user = mysql_user, passwd = mysql_pass, port = int(mysql_port))
                    field_name = "job_name, job_name_row, subitems_name, laster_build_num"
                    field_args ='"' + subitems_name_tmp.strip('/') + '", ' + '"' + self.job_name + '", ' + '"' + subitems_name_tmp + '", ' + '"' + build_num + '"' 
                    field_update = ""
                    args_list = ["branch_parents", "ftp_path", "mvn_args"]
                    for i in self.args.keys():
                        if i in args_list:
                            field_name = field_name + ", " + i 
                            field_args = field_args + ', ' + '"' + ','.join(self.args[i]) + '"' 
                            if field_update:
                                field_update = field_update + ', '  + i + "=" + '"' + ','.join(self.args[i]) + '"'
                            else:
                                field_update = field_update + i + "=" + '"' + ','.join(self.args[i]) + '"'
                    field_update = field_update + ", laster_build_num=" + '"' + build_num +'"'
                    sql_insert = "insert INTO jenkins_info.job_args ({}) VALUES ({});".format(field_name, field_args)
                    sql_update = "update jenkins_info.job_args set {} where job_name = {}".format(field_update, '"' + subitems_name_tmp + '"')
                    sql_check = "select count(*) from jenkins_info.job_args where job_name = {}".format('"' + subitems_name_tmp.strip('/') + '"')
                    cursor = db.cursor()
                    try:
                        cursor.execute(sql_check)
                        if cursor.fetchall()[0][0] < 1:
                            cursor.execute(sql_insert)
                        else:
                            # print(sql_update)
                            if field_update:
                                cursor.execute(sql_update)
                            else:
                                print("update sql 语句键值为空")
                    except:
                        print("判断表中记录存在的sql执行错误")
                    db.commit()
                    db.close()

            else:
                db = pymysql.connect(host = mysql_host, user = mysql_user, passwd = mysql_pass, port = int(mysql_port))
                field_name = "job_name, job_name_row"
                field_args = '"' + self.job_name + '", ' + '"' + self.job_name + '"'
                field_update = ""
                args_list = ["branch_parents", "ftp_path", "mvn_args", "subitems_name"]
                for i in self.args.keys():
                    if i in args_list:
                        field_name = field_name + ", " + i 
                        field_args = field_args + ', ' + '"' + ','.join(self.args[i]) + '"' 
                        if field_update:
                            field_update = field_update + ', '  + i + "=" + '"' + ','.join(self.args[i]) + '"'
                        else:
                            field_update = field_update + i + "=" + '"' + ','.join(self.args[i]) + '"'
                        
                sql_insert = "insert INTO jenkins_info.job_args ({}) VALUES ({});".format(field_name, field_args)
                sql_update = "update jenkins_info.job_args set {} where job_name = {}".format(field_update, '"' + self.job_name + '"')
                sql_check = "select count(*) from jenkins_info.job_args where job_name = {}".format('"' + self.job_name + '"')
                try:
                    cursor = db.cursor()
                    cursor.execute(sql_check)
                    if cursor.fetchall()[0][0] < 1:
                        cursor.execute(sql_insert)
                    else:
                        # print(sql_update)
                        if not field_update:
                            print("update sql 语句键值为空")
                        else:
                            cursor.execute(sql_update)
                except:
                    print("判断表中记录存在的sql执行错误")
                db.commit()
                db.close()
        if self.current_data == "script" and self.name == "ftp_path":
            self.time_tag = time.strftime("%Y%m%d", time.localtime())
            comp = re.compile(r"grep\s(\w*)", re.I|re.M)
            time_tag = time.strftime("%w", time.localtime())
            try:
                self.ftp_file_tag = re.search(comp, self.content).group(1)
                # import pdb; pdb.set_trace()
            except:
                print(self.job_name + ": 检查ftp_path配置，是否符合正则规则")
            if not self.ftp_file_tag + "_v" + time_tag + "_" + self.time_tag in self.args["ftp_path"]:
                self.args["ftp_path"].append(self.ftp_file_tag + "_v" + time_tag + "_" + self.time_tag)
        

    # 元素中内容
    def characters(self, content):
        self.content += content

        if self.current_data == "name":
            # import pdb; pdb.set_trace()
            if content.strip(): 
                self.name= content
                if not content in self.args:
                    self.args[content] = []

        if self.current_data == "string" and self.name ==  "mvn_args":
            # import pdb; pdb.set_trace()
            if content.strip():
                self.args["mvn_args"].append(content)
                             
        if self.current_data == "defaultValue" and self.name == "branch_parents":
            if content.strip():
                self.args["branch_parents"].append(content)

        if self.current_data == "script" and self.name == "subitems_name":
            if content.strip():
                try:
                    f = open('/app/jenkins/jobs/' + self.job_name + '/config.xml')
                    file = f.readlines()
                    get_url_cmd = re.search(r'&apos;(cd.*?)&apos', str(file), re.I|re.M).groups()[0].replace('&quot;', '"')
                    f.close()
                    subitems_name = subprocess.getoutput(get_url_cmd).split()
                    if subitems_name:
                        self.args["subitems_name"] = subitems_name
                except:
                    print(self.job_name + ": 该项目有子目录，jenkins所在服务器未拉取代码")
                    
        if self.current_data == "script" and self.name == "deploy_preprod":
            self.args["deploy_preprod"] = ['yes', 'no']

class  getJenkinsArgs():
    def __init__(self, file_name, job_name):
        self.job_name = job_name
        self.file_name = file_name
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        Handler = getArgs(job_name)
        parser.setContentHandler(Handler)
        parser.parse(file_name)
        

if __name__ == "__main__":
    obj = getJenkinsArgs("config.xml", 'test')
    
