# -*- coding:utf-8 -*-
import os
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

reload(sys)
sys.setdefaultencoding('utf-8')
from .form import CodeUpCnfForms, ExcludeParameterForms, ExecuteCnfForms
from .models import Code_updates_config, Exclude_parameter, Execute_script_config


@login_required(login_url="/accounts/login/")
def exclude_parameter_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        form = ExcludeParameterForms()
        ex_parameter = Exclude_parameter.objects.all()
        return render(request, 'configspec/exclude_parameter_config.html', locals())

    elif request.POST:
        form = ExcludeParameterForms(request.POST)
        if form.is_valid():
            exclude_name = request.POST['exclude_name']
            exclude_parameter = request.POST['exclude_parameter']

            if Exclude_parameter.objects.filter(exclude_name=exclude_name):
                Exclude_parameter.objects.filter(exclude_name=exclude_name).update(exclude_parameter=exclude_parameter)
            else:
                Exclude_parameter(exclude_name=exclude_name, exclude_parameter=exclude_parameter).save()
            return HttpResponseRedirect("/configspec/exclude_parameter_config/")
        else:
            return render(request, 'configspec/exclude_parameter_config.html', locals())
        return render(request, 'configspec/exclude_parameter_config.html', locals())


@login_required(login_url="/accounts/login/")
def code_updates_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        form = CodeUpCnfForms()
        code_up_cnf = Code_updates_config.objects.all()
        ex_config = Exclude_parameter.objects.all()
        return render(request, 'configspec/code_updates_config.html', locals())
    elif request.POST:
        form = CodeUpCnfForms(request.POST)
        if form.is_valid():
            project_name = request.POST['project_name']
            sync_path = str(request.POST['sync_path'])
            sync_module = str(request.POST['sync_module'])
            exclude_parameter_id = request.POST['exclude_parameter_id']
            target_host = ','.join(request.POST.getlist('target_host'))
            if sync_path.endswith('/'):
                if Code_updates_config.objects.filter(project_name=project_name):
                    Code_updates_config.objects.filter(project_name=project_name).update(sync_path=sync_path,
                                                                                         sync_module=sync_module,
                                                                                         exclude_parameter_id=exclude_parameter_id,
                                                                                         target_host=target_host)
                else:
                    Code_updates_config(project_name=project_name, sync_path=sync_path, sync_module=sync_module,
                                        exclude_parameter_id=exclude_parameter_id,
                                        target_host=target_host).save()
            else:
                if Code_updates_config.objects.filter(project_name=project_name):
                    Code_updates_config.objects.filter(project_name=project_name).update(
                        sync_path=sync_path + '/',
                        sync_module=sync_module,
                        exclude_parameter_id=exclude_parameter_id,
                        target_host=target_host)
                else:
                    Code_updates_config(project_name=project_name, sync_path=sync_path + '/',
                                        sync_module=sync_module,
                                        exclude_parameter_id=exclude_parameter_id,
                                        target_host=target_host).save()
            return HttpResponseRedirect("/configspec/code_updates_config/")
        else:
            return render(request, 'configspec/code_updates_config.html', {'form': form})


@login_required(login_url="/accounts/login/")
def execute_script_config(request):
    userid = request.user.id
    level = User.objects.get(id=userid).userprofile.level
    if request.method == 'GET':
        form = ExecuteCnfForms()
        ex_script_cnf = Execute_script_config.objects.all()
        return render(request, 'configspec/execute_script_config.html', locals())
    elif request.POST:
        form = ExecuteCnfForms(request.POST)
        if form.is_valid():
            execute_program = str(request.POST['execute_program'])
            script_name = request.POST['script_name']
            script_path = request.POST['script_path']
            script_note = request.POST['script_note']
            script_permissions = request.POST['script_permissions']
            if Execute_script_config.objects.filter(script_name=script_name):
                print execute_program
                Execute_script_config.objects.filter(script_name=script_name).update(execute_program=execute_program,
                                                                                     script_path=script_path,
                                                                                     script_name=script_name,
                                                                                     script_note=script_note,
                                                                                     script_permissions=script_permissions)
                return HttpResponseRedirect("/configspec/execute_script_config/")
            else:
                print execute_program
                Execute_script_config(execute_program=execute_program, script_name=script_name, script_path=script_path,
                                      script_note=script_note, script_permissions=script_permissions).save()
            return HttpResponseRedirect("/configspec/execute_script_config/")
        else:
            return render(request, 'configspec/execute_script_config.html', locals())

@login_required(login_url="/accounts/login/")
def del_up_config(request):
    id = request.GET['id']
    code_up_cnf = Code_updates_config.objects.get(id=id)
    code_up_cnf.delete()
    return HttpResponseRedirect("/configspec/code_updates_config/")


@login_required(login_url="/accounts/login/")
def del_ex_config(request):
    id = request.GET['id']
    ex_cnf = Exclude_parameter.objects.get(exclude_name=id)
    try:
        os.remove(ex_cnf.file_path)
    except:
        pass
    ex_cnf.delete()
    return HttpResponseRedirect("/configspec/exclude_parameter_config/")
