import os

from django.core.wsgi import get_wsgi_application

import  django.core.handlers.wsgi
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "juziom.settings")

application = django.core.handlers.wsgi.WSGIHandler()

