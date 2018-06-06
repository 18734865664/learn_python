import commands
import time

from celery import task

from dashboard.models import *
from histrecord.models import Sync_history, Exe_script_history
from libtools.salt_api import *
from libtools.send_mail import Updatesendmail
from saltminions.models import *


@task()
def sendtomail(chname, obname, taskid, mailto, message, cc):
    #    print mailto+message+cc
    return Updatesendmail(chname, obname, taskid, mailto, message, cc)


@task()
def grains_task():
    # grains data save to mysql
    sapi = SaltAPI()
    status = sapi.runner_status('status')
    status_up = status['up']
    for host_name in status_up:
        grains = sapi.remote_noarg_execution(host_name, 'grains.items')
        try:
            Salt_grains.objects.get(minion_id=host_name)
        except:
            salt_grains = Salt_grains()
            salt_grains.grains = grains
            salt_grains.minion_id = host_name
            salt_grains.save()
        Salt_grains.objects.filter(minion_id=host_name).update(grains=grains, minion_id=host_name)
        print "Update " + host_name + " grains"


@task()
def minions_status_task():
    # minion status , version data save to mysql
    sapi = SaltAPI()
    status_all = sapi.runner_status('status')
    for host_name in status_all['up']:
        salt_grains = Salt_grains.objects.filter(minion_id=host_name)
        try:
            version = eval(salt_grains[0].grains).get('saltversion').decode('string-escape')
        except:
            version = 'NULL'
            print "No minion version get"
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            status = Minions_status()
            status.minion_id = host_name
            status.minion_version = version
            status.minion_status = 'Up'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version,
                                                                  minion_status='Up')
    for host_name in status_all['down']:
        salt_grains = Salt_grains.objects.filter(minion_id=host_name)
        try:
            version = eval(salt_grains[0].grains).get('saltversion').decode('string-escape')
        except:
            version = 'NULL'
            print "No minion version get"
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            status = Minions_status()
            status.minion_id = host_name
            status.minion_version = version
            status.minion_status = 'Down'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version,
                                                                  minion_status='Down')


@task()
def accept_grains_task(minion_id):
    # when accept key save grains to mysql
    time.sleep(30)
    sapi = SaltAPI()
    grains = sapi.remote_noarg_execution(minion_id, 'grains.items')
    salt_grains = Salt_grains()
    salt_grains.grains = grains
    salt_grains.minion_id = minion_id
    salt_grains.save()
    print "accept " + minion_id + " key"


@task()
def dashboard_task():
    # minion status data save to mysql
    sapi = SaltAPI()
    status = sapi.runner_status('status')
    key_status = sapi.list_all_key()
    up = len(status['up'])
    down = len(status['down'])
    accepted = len(key_status['minions'])
    unaccepted = len(key_status['minions_pre'])
    rejected = len(key_status['minions_rejected'])
    dashboard_status = Dashboard_status()
    try:
        Dashboard_status.objects.get(id=1)
    except:
        dashboard_status.id = 1
        dashboard_status.up = up
        dashboard_status.down = down
        dashboard_status.accepted = accepted
        dashboard_status.unaccepted = unaccepted
        dashboard_status.rejected = rejected
        dashboard_status.save()
    Dashboard_status.objects.filter(id=1).update(id=1, up=up, down=down, accepted=accepted, unaccepted=unaccepted,
                                                 rejected=rejected)


@task()
def sync_code(project_name, sync_module, exclude_parameter, change_content, target_host, sync_path, username):
    sapi = SaltAPI()
    rsync_user = settings.RSYNC_USER
    rsync_passwd = settings.RSYNC_PASSWD
    rsync_server = settings.RSYNC_SERVER
    status0, Current_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(str(sync_path)))
    status1, git_pull = commands.getstatusoutput(
        'cd {0} && git pull >/dev/null 2>&1'.format(sync_path))
    status2, Sync_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(sync_path))
    cmd = '''/usr/bin/rsync -vzrtdm --delete  {ex_parameter} {rsync_user}@{rsync_server}::{sync_module}  {sync_path} --password-file={rsync_passwd}'''.format(
        ex_parameter=exclude_parameter, rsync_user=rsync_user, rsync_server=rsync_server,
        sync_module=sync_module, sync_path=sync_path, rsync_passwd=rsync_passwd)
    jobid,hist_content = sapi.sync_code_hist(target_host, cmd)
    obj = Sync_history(project_name=project_name, change_content=change_content, job_id=jobid,
                       current_commit=Current_commit,
                       sync_commit=Sync_commit, pull_code_status=status1,
                       username=username,hist_content=hist_content)
    obj.save()
    return jobid

@task()
def deliver_config(project_name,cms_hostname,config_file,config_name,restart_server,change_content,username):
    sapi = SaltAPI()
    rsync_user = settings.RSYNC_USER
    rsync_passwd = settings.RSYNC_PASSWD
    rsync_server = settings.RSYNC_SERVER
    status0, Current_commit = commands.getstatusoutput('cd /code/test/config/ && git log -1 --pretty="%h"')
    status1, git_pull = commands,getstatusoutput('cd /code/test/config/ && git pull > /dev/null 2>&1')
    status2, sync_commit = commands.getstatusoutput('cd /code/test/config/ &&   git log -1 --pretty="%h"')
    cmd = '''/usr/bin/rsync -vzrtdm --delete {rsync_user}@{rsync_server}::/code/test/config/{config_name}  {config_file}  --password-file={rsync_passwd}'''.format(rsync_user=rsync_user,rsync_server=rsync_server,config_name=config_name,config_file=config_file,rsync_passwd=rsync_passwd)
    jobid,hist_content = sapi.deliver_config_hist(cms_hostname, cmd)
    obj = Sync_history(project_name=project_name,change_content=change_content,job_id=jobid,current_commit=current_commit,sync_commit=sync_commit,pull_code_status=status1,username=username,hist_content=hist_content)
    obj.save()
    return jobid

@task()
def rollback_code(project_name, sync_module, exclude_parameter, change_content, target_host, sync_path,
                  rollback_commit, username):
    sapi = SaltAPI()
    rsync_user = settings.RSYNC_USER
    rsync_passwd = settings.RSYNC_PASSWD
    rsync_server = settings.RSYNC_SERVER
    status0, Current_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(str(sync_path)))
    status1, git_pull = commands.getstatusoutput(
        'cd {0} && git reset --hard {1} >/tmp/git_pull_log.log 2>&1'.format(
            sync_path, rollback_commit))
    status2, Sync_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(sync_path))
    cmd = '''/usr/bin/rsync -vzrtdm --delete  {ex_parameter} {rsync_user}@{rsync_server}::{sync_module}  {sync_path} --password-file={rsync_passwd}'''.format(
        ex_parameter=exclude_parameter, rsync_user=rsync_user, rsync_server=rsync_server,
        sync_module=sync_module, sync_path=sync_path, rsync_passwd=rsync_passwd)
    jobid = sapi.sync_code(target_host, cmd)
    obj = Sync_history(project_name=project_name, change_content=change_content, job_id=jobid,
                       current_commit=Current_commit,
                       sync_commit=Sync_commit, pull_code_status=status1, username=username)
    obj.save()
    return jobid


@task()
def execute_scripts(execute_program, script_file, target_host, username):
    sapi = SaltAPI()

    cmd = '''{0} {1}'''.format(execute_program, script_file)
    jobid = sapi.remote_execution_async(target_host, cmd)
    obj = Exe_script_history(script_file=script_file, job_id=jobid, username=username)
    obj.save()
    return jobid


@task
def restart_service(sync_path, target_host, username):
    sapi = SaltAPI()

    cmd = '''cd {0} && [[ -f service.sh ]] && /bin/bash service.sh restart && echo "The service script not found." '''.format(
        sync_path)
    jobid = sapi.remote_execution_async(target_host, cmd)
    obj = Exe_script_history(script_file='service.sh', job_id=jobid, username=username)
    obj.save()
    return jobid


@task()
def sync_code_restart_service(project_name, sync_module, exclude_parameter, change_content, target_host, sync_path,
                              username):
    sapi = SaltAPI()
    rsync_user = settings.RSYNC_USER
    rsync_passwd = settings.RSYNC_PASSWD
    rsync_server = settings.RSYNC_SERVER
    status0, Current_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(str(sync_path)))
    status1, git_pull = commands.getstatusoutput(
        'cd {0} && git pull >/dev/null 2>&1'.format(sync_path))
    status2, Sync_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(sync_path))
    cmd = '''/usr/bin/rsync -vzrtdm --delete  {ex_parameter} {rsync_user}@{rsync_server}::{sync_module}  {sync_path} --password-file={rsync_passwd} && cd {sync_path} && [[ -f service.sh ]] && /bin/bash service.sh restart && echo "Update and restart service has sucessed." || echo "Has some error."'''.format(
        ex_parameter=exclude_parameter, rsync_user=rsync_user, rsync_server=rsync_server,
        sync_module=sync_module, sync_path=sync_path, rsync_passwd=rsync_passwd)
    jobid = sapi.sync_code(target_host, cmd)
    obj = Sync_history(project_name=project_name, change_content=change_content, job_id=jobid,
                       current_commit=Current_commit,
                       sync_commit=Sync_commit, pull_code_status=status1, username=username)
    obj.save()
    return jobid


@task()
def rollback_code_restart_service(project_name, sync_module, exclude_parameter, change_content, target_host, sync_path,
                                  rollback_commit, username):
    sapi = SaltAPI()
    rsync_user = settings.RSYNC_USER
    rsync_passwd = settings.RSYNC_PASSWD
    rsync_server = settings.RSYNC_SERVER
    status0, Current_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(str(sync_path)))
    status1, git_pull = commands.getstatusoutput(
        'cd {0} && git reset --hard {1} >/tmp/git_pull_log.log 2>&1'.format(
            sync_path, rollback_commit))
    status2, Sync_commit = commands.getstatusoutput('cd {0} && git log -1  --pretty="%h"'.format(sync_path))
    cmd = '''/usr/bin/rsync -vzrtdm --delete  {ex_parameter} {rsync_user}@{rsync_server}::{sync_module}  {sync_path} --password-file={rsync_passwd} && cd {sync_path} && [[ -f service.sh ]] && /bin/bash service.sh restart && echo "Update and restart service has sucessed." || echo "Has some error."'''.format(
        ex_parameter=exclude_parameter, rsync_user=rsync_user, rsync_server=rsync_server,
        sync_module=sync_module, sync_path=sync_path, rsync_passwd=rsync_passwd)
    jobid = sapi.sync_code(target_host, cmd)
    obj = Sync_history(project_name=project_name, change_content=change_content, job_id=jobid,
                       current_commit=Current_commit,
                       sync_commit=Sync_commit, pull_code_status=status1, username=username)
    obj.save()
    return jobid


@task()
def deliver_cms_config(file_name,software_name,deliver_host,whether_to_reload):
    args = software_name  + '.' + file_name + '_' + whether_to_reload
    sapi = SaltAPI()
    deploy_result_content = sapi.deploy(deliver_host,args )

    return deploy_result_content


@task()
def checking_cms_config(file_name,software_name,deliver_host):
    args = software_name  + '.' + file_name + '_checking'
    sapi = SaltAPI()
    checking_result_content = sapi.deploy(deliver_host,args)
    return checking_result_content


