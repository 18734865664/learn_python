#!/bin/bash
#scl enable python27 bash
UWSGI_PATH="/usr/sbin/uwsgi"
APP_ROOT="/data/juziom/"
cd $APP_ROOT
if [ $1 = "restart" ]; then
    ps -ef |grep juziom.ini |grep -v grep|awk '{print $2}'|xargs kill -9
    sleep 1
cd $APP_ROOT && nohup    uwsgi --ini /data/juziom/juziom.ini  &

fi

#nohup /opt/rh/python27/root/usr/bin/python /data/juziom/manage.py celery worker -B --loglevel=info --settings=juziom.settings --pythonpath=. --logfile=/data/juziom/logs/celery.log &

