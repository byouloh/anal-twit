import os

DEBUG = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_ROOT = os.path.join(PROJECT_ROOT, 'templates')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
SOCKET_URL = '/socket/'

try: from local_settings import *
except: pass
