"""
WSGI config for CraigBotWebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CraigBotWebsite.settings')

_application = get_wsgi_application()

env_variables_to_pass = ['DJANGO_SECRET_KEY', 'CELERY_BROKER', 'TEST_VAR', ]


def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)
