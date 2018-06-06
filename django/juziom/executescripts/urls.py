from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'common_commands', views.common_commands, name='common_commands'),
    url(r'get_script_list(.*)(.*)$', views.get_script_list, name='get_script_list'),
]
