from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^code_updates/$', views.code_updates, name='code_updates'),
    url(r'^code_rollback/$', views.code_rollback, name='code_rollback'),
    url(r'^code_updates/get_cnf_list(.*)$', views.get_cnf_list, name='get_cnf_list'),
    url(r'^get_rollback_commit(.*)$', views.get_rollback_commit, name='get_rollback_commit'),
]
