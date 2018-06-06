import json
import logging
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, RequestContext

from dashboard.models import *
from libtools.check_service import CheckPort, CheckProgress
from saltminions.models import *
from tasks.tasks import dashboard_task, minions_status_task

logger = logging.getLogger('django')


@login_required(login_url="/accounts/login/")
def index(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    try:
        dashboard_task.delay()
        #grains_task.delay()
        minions_status_task.delay()
    except:
        logger.error("Connection refused, don't connect rabbitmq service")
    try:
        dashboard_status = Dashboard_status.objects.get(id=1)
    except:
        status_list = [0, 0, 0, 0, 0]
    else:
        status_list = [int(dashboard_status.up),
                   int(dashboard_status.down),
                   int(dashboard_status.accepted),
                   int(dashboard_status.unaccepted),
                   int(dashboard_status.rejected),
                   ]
        logger.info(status_list)

    salt_grains = Salt_grains.objects.all()
    release_list = []
    os_all = []
    os_release = []
    for release in salt_grains:
        release_dic = eval(str(release.grains))
        if release_dic != None:
            release_info = release_dic.get('osfullname').decode('string-escape') + release_dic.get('osrelease').decode(
                'string-escape')
            release_list.append(release_info)
            os_release = list(set(release_list))

    for release_name in os_release:
        os_dic = {'name': release_name, 'value': release_list.count(release_name)}
        os_all.append(os_dic)
        logger.info(os_all)

    salt_master_stauts = CheckPort('Salt Master', '192.168.10.156', 4505)
    salt_api_status = CheckPort('Salt Api', '0.0.0.0', 8888)
    rabbitmy_status = CheckPort('RabbitMQ', '127.0.0.1', 5672)
    rabbitmy_m_status = CheckPort('RabbitMQ Management', '127.0.0.1', 15672)
    celery_status = CheckProgress('Celery', 'celery worker')
    rsync_status = CheckProgress('Rsync', 'rsync --daemon')
    check_service = [salt_master_stauts, salt_api_status, rabbitmy_status, rabbitmy_m_status, celery_status,
                     rsync_status]


    return render(request, 'index.html', {'status': status_list,
                                                    'os_release': os_release,
                                                    'os_all': os_all,
                                                    'check_service': check_service,
                                          'level': level,
                                          }, context_instance=RequestContext(request))


def get_queue(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    queue_count = []
    time_list = []
    queue_len = len(Dashboard_queue.objects.all())
    if queue_len < 6:
        queue_all = Dashboard_queue.objects.all()[:6]
    else:
        queue_all = Dashboard_queue.objects.all()[queue_len-6:queue_len]
    for i in queue_all:
        queue_count.append(int(i.count))
        time_list.append(i.update_time.decode('string-escape'))
    if len(queue_count) == 0:
        queue_count = [0]
        time_list = [time.strftime('%H:%M', time.localtime())]

    return HttpResponse(json.dumps({"time_list": time_list, "queue_count": queue_count, 'level': level}),
                        content_type='application/json')
