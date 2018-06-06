#! /usr/local/python3/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180522

import xml.sax

setting_type= ['hudson.model.StringParameterDefinition', 'org.biouno.unochoice.ChoiceParameter', 'projectName', 'hudson.model.ChoiceParameterDefinition']

class JobPropertiesHandler( xml.sax.ContentHandler):
    def __init__(self):
        self.project_name = ""
        self.deploy_preprod = ""
        self.mvn_args = ""
        self.ftp_path = ""
        self.choice_env = ""
        self.branche_parents = ""
        self.subitems_name = ""
        self.settle_type = ""
        self.tag = ""
        self.defaultValue = ""
        self.name = ""
        


    # 元素开始事件处理
    def startElement(self, name, attrs):
        self.tag = name
        if self.tag == "hudson.model.StringParameterDefinition":
            self.settle_type = self.tag
        if self.tag == "org.biouno.unochoice.ChoiceParameter":
            self.settle_type = self.tag


    # 元素结束事件处理
    def endElement(self, name):
        if name == "properties":
            print( self.name)
            # import pdb; pdb.set_trace()
   
    
    # 内容事件处理
    def characters(self, content):
        if self.tag == "name" and  content.strip():
            self.name = self.name + ', ' + content.strip()
        #    import pdb; pdb.set_trace()
        if self.tag == "defaultValue":
            self.defaultValue = content
        if self.tag == "projectName":
            self.project_name = content
        
        
        
        
if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = JobPropertiesHandler()
    parser.setContentHandler( Handler )
    parser.parse("config.xml")
