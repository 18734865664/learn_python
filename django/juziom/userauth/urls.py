from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^$', include('dashboard.urls')),
]