# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1040851/data/www/questionless.net/askme')
sys.path.insert(1, '/var/www/u1040851/data/venv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'askme.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
