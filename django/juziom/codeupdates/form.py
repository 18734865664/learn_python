# -*- coding:utf-8 -*-

from django import forms
from configspec.models import Code_updates_config


def Get_project():
    project_from_sql = Code_updates_config.objects.all().values('id', 'project_name')
    project_list = []
    for i in project_from_sql:
        plist = (str(i['id']), i['project_name'])
        project_list.append(plist)
    return project_list

class CodeUpForms(forms.Form):
    project_name = forms.ChoiceField(label=u'项目名称', widget=forms.Select(
        attrs={'class': 'form-control', 'onchange': 'getcnfoptions(this.value)'}),
                                     choices=([(u'', u'选择项目')] + Get_project()),
                                     error_messages={'required': u'请选择项目名称'})
    sync_path = forms.CharField(label=u'同步路径', max_length=255,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
                                error_messages={'required': u'路径不能为空'})
    sync_module = forms.CharField(label=u'同步模块', max_length=255,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
                                  error_messages={'required': u'不能为空'})
    change_content = forms.CharField(label=u'变更内容', max_length=2048,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     error_messages={'required': u'内容不能为空'})

    exclude_parameter = forms.CharField(label=u'过滤参数',
                                        widget=forms.Textarea(
                                            attrs={'class': 'form-control', 'rows': "4", 'readonly': ''}),
                                        error_messages={'required': u'内容不能为空'})

    restart_service = forms.ChoiceField(label=u'重启服务', widget=forms.RadioSelect(attrs={'type': 'radio'}),
                                        choices=(('yes', u'是'), ('no', u'否')), initial='no')

class CodeRoForms(forms.Form):
    project_name = forms.ChoiceField(label=u'项目名称', widget=forms.Select(
        attrs={'class': 'form-control', 'onchange': 'getcnfoptions(this.value)', 'name': 'cnfid'}),
                                     choices=([(u'', u'选择项目')] + Get_project()),
                                     error_messages={'required': u'请选择项目名称'})
    sync_path = forms.CharField(label=u'回滚路径', max_length=255,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
                                error_messages={'required': u'路径不能为空'})
    sync_module = forms.CharField(label=u'回滚模块', max_length=255,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
                                  error_messages={'required': u'不能为空'})
    exclude_parameter = forms.CharField(label=u'过滤参数',
                                        widget=forms.Textarea(
                                            attrs={'class': 'form-control', 'rows': "4", 'readonly': ''}),
                                        error_messages={'required': u'内容不能为空'})
    change_content = forms.CharField(label=u'变更内容', max_length=2048,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     error_messages={'required': u'内容不能为空'})
    restart_service = forms.ChoiceField(label=u'重启服务', widget=forms.RadioSelect(attrs={'type': 'radio'}),
                                        choices=(('yes', u'是'), ('no', u'否')), initial='no')

# rollback_commit = forms.ChoiceField(label=u'回滚版本',
#                                        error_messages={'required': u'版本不能为空'})
