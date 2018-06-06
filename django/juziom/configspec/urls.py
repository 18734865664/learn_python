from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^exclude_parameter_config', views.exclude_parameter_config, name='exclude_parameter_config'),
    url(r'^code_updates_config', views.code_updates_config, name='code_updates_config'),
    url(r'^execute_script_config', views.execute_script_config, name='execute_script_config'),
    url(r'^del_up_config', views.del_up_config, name='del_up_config'),
    url(r'^del_ex_config', views.del_ex_config, name='del_ex_config'),

]
