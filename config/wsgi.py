import os

from django.core.wsgi import get_wsgi_application
from schedule import start

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
start()
