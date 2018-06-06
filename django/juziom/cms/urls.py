from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cms_config$', views.cms_config, name='cms_config'),
    url(r'^del_cms_config$', views.del_cms_config, name='del_cms_config'),
    url(r'^get_cms_config$', views.get_cms_config, name='get_cms_config'),
    url(r'^get_other_parameter$', views.get_other_parameter, name='get_other_parameter'),
    url(r'^get_backup_other_parameter$', views.get_backup_other_parameter, name='get_backup_other_parameter'),
    url(r'^save_cms_config$', views.save_cms_config, name='save_cms_config'),
    url(r'^cms_deliver$', views.deliver_config, name='deliver_config'),
    url(r'^cms_edit$', views.edit_config, name='edit_config'),
    url(r'^download_file$', views.download_file, name='download_file'),
    url(r'^checking_cms_config$', views.checking_cms_config,name='checking_cms_config'),
    url(r'^get_file_name$', views.get_file_name,name='get_file_name'),
    url(r'^save_config$', views.save_config,name='save_config'),
]
