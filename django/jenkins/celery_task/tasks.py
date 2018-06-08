#! /usr/local/python3/bin/python
# encoding=utf8

from celery import Celery, task
from time import sleep

# 直接利用celery
# app = Celery('tasks', backend = 'amqp://guest:guest@localhost:5672//', broker='amqp://guest:guest@localhost:5672//')

# @app.task
# def add(x, y):
#     return x + y


@task
def add(x, y):
    sleep(3)
    return x + y
