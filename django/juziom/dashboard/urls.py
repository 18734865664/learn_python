from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'get_queue', views.get_queue, name='get_queue'),
]