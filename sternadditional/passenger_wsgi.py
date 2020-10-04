# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/j/jeiska228/vityazgroup.queegree.ga/public_html/stern-olympiad-master')
sys.path.insert(1, '/home/j/jeiska228/vityazgroup.queegree.ga/public_html/venv/lib/python3.6/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sternadditional.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()