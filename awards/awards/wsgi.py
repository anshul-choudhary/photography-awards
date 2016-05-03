"""
WSGI config for xcellinsproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
import site

site.addsitedir('/root/.virtualenvs/awards/lib/python2.7/site-packages')
sys.path.append('/var/www/awards')
sys.path.append('/root/.virtualenvs/awards/lib/python2.7/site-packages')
sys.path.append('/root/.virtualenvs/awards/lib/python2.7/site-packages/django/contrib/admindocs')
sys.path.append('/root/.virtualenvs/awards/lib/python2.7/site-packages/django')

os.environ['DJANGO_SETTINGS_MODULE'] = 'awards.settings'

try:
    activate_env=os.path.expanduser(
        "/root/.virtualenvs/awards/bin/activate_this.py")
    execfile(activate_env, dict(__file__=activate_env))
except:
    pass


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()