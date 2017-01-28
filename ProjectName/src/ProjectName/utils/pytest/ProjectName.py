import mock
import os

from django.conf import settings


def pytest_configure(config):
    # HACK: Only needed for testing!
    os.environ.setdefault('_<% project_name|upper %>_SKIP_CONFIGURATION', '1')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<% project_name %>.conf.server')

    if not settings.configured:
        # only configure the db if its not already done
        test_db = os.environ.get('DB', 'sqlite')
        if test_db == 'postgres':
            settings.DATABASES['default'].update({
                'ENGINE': 'django.db.backends.postgresql',
                'USER': '<% project_name %>',
                'NAME': '<% project_name %>',
            })
        elif test_db == 'sqlite':
            settings.DATABASES['default'].update({
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            })
        else:
            raise RuntimeError('oops, wrong database: %r' % test_db)

    settings.TEMPLATE_DEBUG = True
    # Disable static compiling in tests
    settings.STATIC_BUNDLES = {}
    # override a few things with our test specifics
    settings.INSTALLED_APPS = tuple(settings.INSTALLED_APPS) + (
        'tests',
    )
    # This speeds up the tests considerably, pbkdf2 is by design, slow.
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    settings.AUTH_PASSWORD_VALIDATORS = []
    settings.DEBUG_VIEWS = True
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    # django mail uses socket.getfqdn which doesn't play nice if our networking isn't stable
    patcher = mock.patch('socket.getfqdn', return_value='localhost')
    patcher.start()

    from django.core.cache import cache
    cache.clear()


def pytest_runtest_teardown(item):
    from django.core.cache import cache
    cache.clear()
