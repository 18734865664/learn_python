#! /usr/local/python3/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180523

import xml.sax
import re
import time
import pymysql
import sys
sys.path.insert(0, '/data/nfs/python/learn_python/jenkins/')
from get_file_list import getFileList

""" 
getArgs: 
get: 用来获取jenkins job配置文件，xml格式

"""

mysql_host = "10.100.137.179"
mysql_user = "root"
mysql_pass = "123123"
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
    
    def startElement(self, name, args):
        self.current_data = name
        if self.current_data == "script" and self.name == "ftp_path":
            self.content = ""

    def endElement(self, name):
        # if name == "string":
        #     import pdb; pdb.set_trace()
        #     print(self.args["mvn_args"])
        if name == "properties":
            db = pymysql.connect(host = mysql_host, user = mysql_user, passwd = mysql_pass, port = int(mysql_port))
            field_name = "job_name, job_name_row"
            field_args = '"' + self.job_name.replace("-", "_") + '", ' + '"' + self.job_name + '"'
            field_update = ""
            args_list = ["branch_parents", "ftp_path", "mvn_args", "subitems_name"]
            for i in self.args.keys():
                if i in args_list:
                    field_name = field_name + ", " + i 
                    field_args = field_args + ', ' + '"' + str(self.args[i]) + '"' 
                    if field_update:
                        field_update = field_update + ', '  + i + "=" + '"' + str(self.args[i]) + '"'
                    else:
                        field_update = field_update + i + "=" + '"' + str(self.args[i]) + '"'
                    
            sql_insert = "insert INTO jenkins_info.job_args ({}) VALUES ({});".format(field_name, field_args)
            sql_update = "update jenkins_info.job_args set {} where job_name = {}".format(field_update, '"' + self.job_name.replace("-", "_") + '"')
            sql_check = "select count(*) from jenkins_info.job_args where job_name = {}".format('"' + self.job_name.replace("-", "_") + '"')
            cursor = db.cursor()
            cursor.execute(sql_check)
            if cursor.fetchall()[0][0] < 1:
                cursor.execute(sql_insert)
            else:
                print(sql_update)
                if not field_update:
                    pass
                else:
                    cursor.execute(sql_update)
            db.commit()
            db.close()
        if self.current_data == "script" and self.name == "ftp_path":
            self.time_tag = time.strftime("%Y%m%d", time.localtime())
            comp = re.compile(r"grep\s(\w*)", re.I|re.M)
            try:
                self.ftp_file_tag = re.search(comp, self.content).group(1)
                # import pdb; pdb.set_trace()
            except:
                pass
            if not self.ftp_file_tag + self.time_tag in self.args["ftp_path"]:
                self.args["ftp_path"].append(self.ftp_file_tag + self.time_tag)
        

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
    
