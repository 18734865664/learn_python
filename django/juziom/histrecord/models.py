# -*- coding:utf-8 -*-
from django.db import models

from configspec.models import Code_updates_config


class Sync_history(models.Model):
    class Meta:
        db_table = "sync_history"

    project_name = models.CharField(max_length=255)
    change_content = models.CharField(max_length=2048)
    job_id = models.CharField(max_length=255)
    current_commit = models.CharField(max_length=128)
    sync_commit = models.CharField(max_length=128)
    pull_code_status = models.CharField(max_length=10)
    date_time = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100)
    hist_content = models.TextField()


class Exe_script_history(models.Model):
    class Meta:
        db_table = "exe_script_history"

    script_file = models.CharField(max_length=255)
    job_id = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100)
