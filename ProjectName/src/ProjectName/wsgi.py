import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

from django.conf import settings

if not settings.configured:
    from <% project_name %>.runner import configure
    configure()

application = get_wsgi_application()
