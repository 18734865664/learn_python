# coding:utf-8
from django.db import models

# Create your models here.

class CmsConfig(models.Model):
    class Meta:
        db_table = 'cms_config'
    cms_config_name = models.CharField(max_length=128)
    app_name = models.CharField(max_length=128)
    software_name = models.CharField(max_length=128)
    config_file_name = models.CharField(max_length=128)
    deliver_host = models.TextField()
    config_content = models.TextField()
    def __unicode__(self):
        return u'{} {} {} {} {}'.format(self.cms_config_name,self.app_name,self.software_name,self.config_file_name,self.deliver_host,self.config_content)

class DeliverConfigHistory(models.Model):
    class Meta:
        db_table = "deliver_config_history"
    username = models.CharField(max_length=128)
    config_file_id = models.IntegerField()
    false_num = models.IntegerField()
    deliver_host =  models.TextField()
    history_content = models.TextField()
    whether_to_reload = models.CharField(max_length=128)
    opt_time = models.CharField(max_length=128)
    def __unicode__(self):
         u'{} {} {} {} {} {}'.format(self.username,self.config_file_id,self.deliver_host,self.history_content,self.whether_to_reload,self.opt_time)

class VersionOfConfig(models.Model):
    class Meta:
        db_table = "version_of_config"
    cms_config_id = models.CharField(max_length=128)
    reasons_for_change = models.CharField(max_length=128)
    backup_file_name = models.CharField(max_length=128)
    backup_file_path = models.CharField(max_length=128)
    def __unicode__(self):
         u'{} {} {} {}'.format(self.cms_config_id,self.reasons_for_change,self.backup_file_name,self.backup_file_path)


