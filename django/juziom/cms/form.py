# coding:utf-8
from django import forms
from saltminions.models import Minions_status
from .models import  CmsConfig
from configspec.form import Get_host as get_host
import commands

class CmsConfigForms(forms.Form):
    cms_config_name = forms.CharField(label=u'配置名称',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':u'配置名称不能为空'})
    app_name = forms.CharField(label=u'项目名称',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':u'项目名不能为空'})
    software_name = forms.CharField(label=u'软件名称',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':u'软件名不能为空'})
    config_file_name = forms.CharField(label=u'配置文件路径',max_length=255,widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':u'文件路径不能为空'})
    deliver_host = forms.MultipleChoiceField(label=u'目标主机',widget=forms.SelectMultiple(attrs={'class':"form-control"}),choices=get_host(),error_messages={'required':u"选择主机"})
    config_content = forms.FileField(label=u'配置文件内容',widget=forms.Textarea(attrs={'class':'form-control'}),error_messages={'required':u'内容不能为空'})

def get_cms_config_name():
    return list(CmsConfig.objects.values_list("id","cms_config_name"))



class DeliverConfigForms(forms.Form):
    def __init__(self,*args,**kwargs):
        super(DeliverConfigForms,self).__init__(*args,**kwargs)
        cms_config_name_list = list(CmsConfig.objects.values_list("id","cms_config_name"))
        self.fields['cms_config_name'].widget.choices = [('',u'选择配置项')] + cms_config_name_list
    cms_config_name_list = list(CmsConfig.objects.values_list("id","cms_config_name"))
    cms_config_name = forms.ChoiceField(label=u'配置名称',widget=forms.Select(attrs={'class':'form-control','onchange':"get_file_name(this.value)","name":'deliver_cms_config_name'}),error_messages={'required':u'配置名称不能为空'},choices=([('',u'选择配置项')] + cms_config_name_list))
    app_name =  forms.CharField(label=u'项目名称',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'项目名不能为空'})
    software_name = forms.CharField(label=u'软件名称',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'软件名不能为空'})
    config_file_name = forms.CharField(label=u'配置文件路径',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'文件路径不能为空'})
    reasons_for_change = forms.CharField(label=u'变更原因',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'变更原因不能为空'})
    config_file = forms.FileField(label=u'上传文件',widget=forms.ClearableFileInput(attrs={"class":"form-control"}))

def get_backup_file_name():
    return list(CmsConfig.objects.values_list('id','file_name'))

class EditConfigForms(forms.Form):
    def __init__(self,*args,**kwargs):
        super(EditConfigForms,self).__init__(*args,**kwargs)
        cms_config_name_list = list(CmsConfig.objects.values_list("id","cms_config_name"))
        self.fields['cms_config_name'].widget.choices = [('',u'选择配置项')] +cms_config_name_list
    cms_config_name_list = list(CmsConfig.objects.values_list("id","cms_config_name"))
    cms_config_name =forms.ChoiceField(label=u'配置名称',widget=forms.Select(attrs={'class':'form-control','onchange':"get_other_parameter(this.value)","name":'deliver_cms_config_name'}),error_messages={'required':u'配置名称不能为空'},choices=([('',u'选择配置项')]+cms_config_name_list))
    app_name =  forms.CharField(label=u'项目名称',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'项目名不能为空'})
    software_name = forms.CharField(label=u'软件名称',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'软件名不能为空'})
    config_file_name = forms.CharField(label=u'配置文件路径',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'文件路径不能为空'})
    reasons_for_change = forms.CharField(label=u'变更原因',max_length=255,widget=forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),error_messages={'required':u'变更原因不能为空'})
    config_file = forms.FileField(label=u'上传文件',widget=forms.ClearableFileInput(attrs={"class":"form-control"}))
