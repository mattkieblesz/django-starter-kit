import os
import click
from pkg_resources import resource_string


DEFAULT_CONFIG_DIR = '~/.<% project_name %>'
DEFAULT_SETTINGS_MODULE = '<% project_name %>.conf.server'
DEFAULT_SETTINGS_OVERRIDE = '<% project_name %>.conf.py'


def generate_secret_key():
    from django.utils.crypto import get_random_string
    chars = u'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def load_config_template(path, version='default'):
    return resource_string('<% project_name %>', 'conf/{}.{}'.format(path, version)).decode('utf8')


def generate_settings(dev=False):
    context = {
        'secret_key': generate_secret_key(),
        'debug_flag': dev,
        'mail_backend': 'console' if dev else 'smtp',
        'site_domain': 'localhost:8000' if dev else '<% project_name %>.com'
    }

    return load_config_template(DEFAULT_SETTINGS_OVERRIDE) % context


def get_asset_version(settings):
    path = os.path.join(settings.STATIC_ROOT, 'version')
    try:
        with open(path) as fp:
            return fp.read().strip()
    except IOError:
        from time import time
        return int(time())


def get_<% project_name %>_conf():
    try:
        ctx = click.get_current_context()
        return ctx.obj['config']
    except (RuntimeError, KeyError, TypeError):
        try:
            return os.environ['<% project_name|upper %>_CONF']
        except KeyError:
            return DEFAULT_CONFIG_DIR


def discover_configs():
    try:
        config = os.environ['<% project_name|upper %>_CONF']
    except KeyError:
        config = DEFAULT_CONFIG_DIR

    config = os.path.expanduser(config)

    return (
        config,
        os.path.join(config, DEFAULT_SETTINGS_OVERRIDE),
    )


def configure(ctx, py):
    '''
    Given the two different config files, set up the environment.

    NOTE: Will only execute once, so it's safe to call multiple times.
    '''
    global __installed
    if __installed:
        return

    # Add in additional mimetypes that are useful for our static files which aren't common in default system registries
    import mimetypes
    for type, ext in (
        ('application/json', 'map'),
        ('application/font-woff', 'woff'),
        ('application/font-woff2', 'woff2'),
        ('application/vnd.ms-fontobject', 'eot'),
        ('application/x-font-ttf', 'ttf'),
        ('application/x-font-ttf', 'ttc'),
        ('font/opentype', 'otf'),
    ):
        mimetypes.add_type(type, '.' + ext)

    from .importer import install

    if not os.path.exists(py):
        if ctx:
            raise click.ClickException("Configuration file does not exist. Use '<% project_name %> init' to initialize the file.")
        raise ValueError("Configuration file does not exist at '%s'" % click.format_filename(py))

    # Add autoreload for config.yml file if needed
    if 'UWSGI_PY_AUTORELOAD' in os.environ:
        try:
            import uwsgi
            from uwsgidecorators import filemon
        except ImportError:
            pass
        else:
            filemon(py)(uwsgi.reload)

    os.environ['DJANGO_SETTINGS_MODULE'] = '<% project_name %>_config'

    install('<% project_name %>_config', py, DEFAULT_SETTINGS_MODULE)

    # HACK: we need to force access of django.conf.settings to ensure we don't hit any import-driven recursive behavior
    from django.conf import settings
    hasattr(settings, 'INSTALLED_APPS')

    settings.ASSET_VERSION = get_asset_version(settings)
    settings.STATIC_URL = settings.STATIC_URL.format(
        version=settings.ASSET_VERSION,
    )
    settings.EMAIL_BACKEND = settings.EMAIL_BACKEND_ALIASES[settings.EMAIL_BACKEND]

    from django.utils import timezone
    from <% project_name %>.app import env
    env.data['config'] = get_<% project_name %>_conf()
    env.data['start_date'] = timezone.now()

    __installed = True

    import django
    django.setup()

    # force signal registration
    import <% project_name %>.receivers  # NOQA


__installed = False
