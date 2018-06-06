# -*- coding:utf-8 -*-
from django.db import models


class Exclude_parameter(models.Model):
    class Meta:
        db_table = "exclude_parameter"

    exclude_name = models.CharField(max_length=128)
    exclude_parameter = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.exclude_name, self.exclude_parameter)


class Code_updates_config(models.Model):
    class Meta:
        db_table = "code_updates_config"

    project_name = models.CharField(max_length=128)
    sync_path = models.CharField(max_length=128)
    sync_module = models.TextField()
    target_host = models.TextField()
    exclude_parameter = models.ForeignKey(Exclude_parameter, related_name='code_exclude')

    def __unicode__(self):
        return u'%s %s %s %s %s' % (
            self.project_name, self.sync_path, self.sync_module, self.target_host, self.exclude_parameter)


class Execute_script_config(models.Model):
    class Meta:
        db_table = "execute_script_config"

    execute_program = models.CharField(max_length=128)
    script_name = models.CharField(max_length=128)
    script_path = models.CharField(max_length=255)
    script_note = models.CharField(max_length=255)
    script_permissions = models.CharField(max_length=32)

    def __unicode__(self):
        return u'%s %s %s %s %s' % (
            self.execute_program, self.script_name, self.script_path, self.script_notes, self.script_permissions)
