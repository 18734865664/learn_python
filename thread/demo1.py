#! /usr/local/python3/bin/python3
# encoding: utf-8

import queue
import threading
import time

# 创建队列实例，用于存储任务
queue = queue.Queue()

# 定义需要线程池执行的任务
def do_job():
    while True:
        # lock.acquire()
        i = queue.get()
        time.sleep(1)
        print("index {}, curent: {}".format(i, threading.current_thread()))
        queue.task_done()
        # lock.release()

if __name__ == "__main__":
    # 创建包括3个线程的线程池
    lock = threading.RLock()
    for i in range(3):
        t = threading.Thread(target = do_job)
        t.daemon = True
        t.start()
    
    time.sleep(1)
    for i in range(10):
        queue.put(i)
    
    queue.join()
