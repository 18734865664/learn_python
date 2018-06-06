from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'operarecord', views.sync_history, name='sync_history'),
    url(r'executerecord', views.execute_history, name='sync_history'),
    url(r'getjobscontent(.*)$', views.get_job_content, name='get_job_content'),
    url(r'deliverconfig', views.deliver_config, name='deliver_config'),
    url(r'get_deliver_content', views.get_deliver_content, name='get_deliver_content'),

]
