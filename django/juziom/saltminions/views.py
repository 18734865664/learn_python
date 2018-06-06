from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from libtools.salt_api import *
from saltminions.models import Minions_status, Salt_grains
from tasks.tasks import accept_grains_task, minions_status_task


@login_required(login_url="/accounts/login/")
def minions_status(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    status = Minions_status.objects.all()
    return render(request, 'saltminions/minions_status.html', locals())


@login_required(login_url="/accounts/login/")
def minions_keys(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    sapi = SaltAPI()
    alert_info = ""
    if request.POST:
        minion_id_a = request.POST.get("accept")
        minion_id_r = request.POST.get("reject")
        minion_id_d = request.POST.get("delete")
        if minion_id_a:
            sapi.accept_key(minion_id_a)
            try:
                accept_grains_task.delay(minion_id_a)
            except Exception as e:
                print e
            try:
                minions_status_task.delay()
                alert_info = "Minion: " + minion_id_a + " Accept Key Success"
            except Exception as e:
                alert_info = "Minion: " + minion_id_a + " Accept Key Fault"
                print e
        elif minion_id_r:
            sapi.reject_key(minion_id_r)
        else:
            sapi.delete_key(minion_id_d)
            try:
                Minions_status.objects.get(minion_id=minion_id_d).delete()
            except Exception as e:
                print e
            try:
                Salt_grains.objects.get(minion_id=minion_id_d).delete()
            except Exception as e:
                print e
            try:
                minions_status_task.delay()
                alert_info = "Minion: " + minion_id_d + " Accept Key Success"
            except Exception as e:
                alert_info = "Minion: " + minion_id_d + " Accept Key Fault"
                print e

    keys_all = sapi.list_all_key()

    return render(request, 'saltminions/minions_keys.html', {'key': keys_all, 'alert_info': alert_info, 'level': level})
