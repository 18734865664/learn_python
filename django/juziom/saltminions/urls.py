from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^minions_status', views.minions_status,name='minions_status'),
    url(r'^minions_keys', views.minions_keys,name='minions_keys'),

]