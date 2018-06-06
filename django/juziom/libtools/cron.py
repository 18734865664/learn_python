from salt_api import *
from saltminions.models import *
import subprocess
import time
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

sapi = SaltAPI()


def minions_status_scheduled_job():
    status = Minions_status()
    status_all = sapi.runner_status('status')
    for host_name in status_all['up']:
        salt_grains = Salt_grains.objects.filter(minion_id=host_name)
#        version = eval(salt_grains[0].grains).get('saltversion').decode('string-escape')
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            status.minion_id = host_name
#            status.minion_version = version
            status.minion_status = 'Up'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name,  minion_status='Up')
    for host_name in status_all['down']:
        salt_grains = Salt_grains.objects.filter(minion_id=host_name)
#        version = eval(salt_grains[0].grains).get('saltversion').decode('string-escape')
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            status.minion_id = host_name
            status.minion_version = version
            status.minion_status = 'Down'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name,  minion_status='Down')



def grains_scheduled_job():
    salt_grains = Salt_grains()
    status = Minions_status.objects.filter(minion_status='Up')
    for host_name in status:
        grains = sapi.remote_noarg_execution(host_name.minion_id, 'grains.items')
        try:
            Salt_grains.objects.get(minion_id=host_name.minion_id)
        except:
            salt_grains.grains = grains
            salt_grains.minion_id = host_name.minion_id
            salt_grains.save()
        Salt_grains.objects.filter(minion_id=host_name.minion_id).update(grains=grains, minion_id=host_name.minion_id)


