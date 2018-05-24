#! /usr/local/python3/bin/python3
# encoding: utf-8
# author: qiangguo
# last_modify: 20180523

import xml.sax

class getMvnArgs(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.name = ""
        self.args = {}
        self.tag = 0
    
    def startElement(self, name, args):
        self.current_data = name

    def endElement(self, name):
        if name == "string":
        #     import pdb; pdb.set_trace()
            print(self.args["mvn_args"])
        

    def characters(self, content):
        if self.current_data == "name":
            # import pdb; pdb.set_trace()
            if content.strip(): 
                self.name = content
            self.args[content] = []
        if self.current_data == "string" and  self.name == "mvn_args":
            # import pdb; pdb.set_trace()
            self.tag = 1
            if content.strip():
                self.args[self.name].append(content)
            

if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = getMvnArgs()
    parser.setContentHandler(Handler)
    parser.parse("config.xml")
