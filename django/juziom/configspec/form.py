# -*- coding:utf-8 -*-

from django import forms

from saltminions.models import Minions_status
from .models import Exclude_parameter

CHECKBOX_CHOICES = [['yes', u'是'], ['no', u'否']]
SELECT_CHOICES = Minions_status.objects.all().values('minion_id')


def Get_host():
    host_from_sql = Minions_status.objects.all().values('minion_id')
    host_list = []
    for i in host_from_sql:
        hosts = [i['minion_id'], i['minion_id']]
        host_list.append(hosts)
    return host_list


def Get_ex_parameter():
    parameter_from_sql = Exclude_parameter.objects.all().values('id', 'exclude_name')
    parameter_list = []
    for i in parameter_from_sql:
        plist = (str(i['id']), i['exclude_name'])
        parameter_list.append(plist)
    return parameter_list


def check_ex_file(value):
    pass
    # if 'exclude_file' not in value:
    #    raise forms.ValidationError(u"文件路径填写错误")


class CodeUpCnfForms(forms.Form):
    project_name = forms.CharField(label=u'项目名称', max_length=255,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   error_messages={'required': u'名称不能为空'})
    sync_path = forms.CharField(label=u'同步路径', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                error_messages={'required': u'路径不能为空'})
    sync_module = forms.CharField(label=u'同步模块', max_length=255,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  error_messages={'required': u'模块不能为空'})
    exclude_parameter_id = forms.ChoiceField(label=u'过滤配置', widget=forms.Select(attrs={'class': 'form-control'}),
                                             choices=Get_ex_parameter(), error_messages={'required': u'请选择过滤配置'})
    target_host = forms.MultipleChoiceField(label=u'目标主机', widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                            choices=Get_host(), error_messages={'required': u'请选择目标主机'})


class ExcludeParameterForms(forms.Form):
    exclude_name = forms.CharField(label=u'配置名称', max_length=255,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   error_messages={'required': u'名称不能为空'})
    exclude_parameter = forms.CharField(label=u'参数内容',
                                        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                        error_messages={'required': u'内容不能为空'})


class ExecuteCnfForms(forms.Form):
    execute_program = forms.ChoiceField(label=u'执行程序', widget=forms.Select(
        attrs={'class': 'form-control'}),
                                        choices=([(u'/bin/bash', u'Shell')] + [(u'/bin/python', u'Python')]),
                                        error_messages={'required': u'请选择执行程序'})
    script_name = forms.CharField(label=u'脚本名称',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  error_messages={'required': u'名称不能为空'})
    script_path = forms.CharField(label=u'脚本路径',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  error_messages={'required': u'路径不能为空'})
    script_note = forms.CharField(label=u'脚本备注',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  error_messages={'required': u'备注不能为空'})
    script_permissions = forms.CharField(label=u'执行权限',
                                         widget=forms.TextInput(attrs={'class': 'form-control'}),
                                         error_messages={'required': u'权限不能为空'})
