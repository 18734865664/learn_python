#!/usr/local/python3/bin/python3
# author: qiangguo
# last_modify
# version: v1.0.0

import pika

# 建立连接connection 到 rabbitmq
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

# 创建虚拟连接channel
chann = conn.channel()

# 创建队列
result = chann.queue_declare(queue="anheng", durable=True)


