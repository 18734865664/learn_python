#! /usr/local/python3/bin/python3
# encoding:utf-8
# author: qiangguo
# last_modify

from xml.dom.minidom import parse
import xml.dom.minidom


dom_tree = xml.dom.minidom.parse("config.xml")
collection = dom_tree.documentElement
if collection.hasAttribute("shelf"):
    print("Root element : %s" % collection.getAttribute("shelf"))


properties = collection.getElementsByTagName("hudson.model.ChoiceParameterDefinition")

for i in properties:
    if properties.hasAttribute("name"):
        print("name: {}".format(properties.hasAttribute("name")))
