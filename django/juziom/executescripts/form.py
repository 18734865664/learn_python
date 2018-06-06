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


class ExeScriptForms(forms.Form):
    project_name = forms.ChoiceField(label=u'项目名称', widget=forms.Select(
        attrs={'class': 'form-control', 'onchange': 'getcnfoptions(this.value)'}),
                                     choices=([(u'', u'选择项目')] + Get_project()),
                                     error_messages={'required': u'请选择项目名称'})
