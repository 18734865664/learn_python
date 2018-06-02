#! /usr/local/python3/bin/python3
from django.conf import settings
import jenkins

class build_jenkins_api():
    def __init__(self):
        pass
    
    def build_jenkins_api(self, data):
    # 实例化jenkins
        server = jenkins.Jenkins(settings.JENKINS_URL, username=settings.JENKINS_USERNAME, password = settings.JENKINS_PASSWORD)
        server.build_job(jenkins_build, parameters = data)
