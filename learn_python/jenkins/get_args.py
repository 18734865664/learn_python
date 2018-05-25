#! /usr/local/python3/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180523

import xml.sax
import pymysql
import re
import time

""" 
getArgs: 
get: 用来获取jenkins job配置文件，xml格式

"""
class getArgs(xml.sax.ContentHandler):

    def __init__(self):
        self.current_data = ""
        self.name = []
        self.args = {}
        self.ftp_file_tag = ""
        self.time_tag = ""
        self.content = ""
    
    def startElement(self, name, args):
        self.current_data = name
        if self.current_data == "script" and self.name == "ftp_path":
            self.content = ""

    def endElement(self, name):
        # if name == "string":
        #     import pdb; pdb.set_trace()
        #     print(self.args["mvn_args"])
        if name == "properties":
            print(self.args)
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
    def __init__(self, file_name):
        self.file_name = file_name
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        Handler = getArgs()
        parser.setContentHandler(Handler)
        parser.parse(file_name)
        

if __name__ == "__main__":
    obj = getJenkinsArgs("config.xml")
    
