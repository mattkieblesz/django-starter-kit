import os
import sys


def convert_options_to_env(options):
    for k, v in iter(options.items()):
        if v is None:
            continue
        key = 'UWSGI_' + k.upper().replace('-', '_')
        if isinstance(v, str):
            value = v
        elif v is True:
            value = 'true'
        elif v is False:
            value = 'false'
        elif isinstance(v, int):
            value = str(v)
        else:
            raise TypeError('Unknown option type: %r (%s)' % (k, type(v)))
        yield key, value


class HTTPServer(object):
    name = 'http'

    def __init__(self, host=None, port=None, debug=False, workers=None, validate=True, extra_options=None):
        from django.conf import settings

        host = host or settings.<% project_name|upper %>_WEB_HOST
        port = port or settings.<% project_name|upper %>_WEB_PORT

        options = (settings.<% project_name|upper %>_WEB_OPTIONS or {}).copy()
        if extra_options is not None:
            for k, v in iter(extra_options.items()):
                options[k] = v

        # uWSGI default options
        options.setdefault('module', '<% project_name %>.wsgi:application')
        options.setdefault('protocol', 'http')
        options.setdefault('auto-procname', True)
        options.setdefault('procname-prefix-spaced', '[<% project_name %>]')
        options.setdefault('workers', 3)
        options.setdefault('threads', 4)
        options.setdefault('http-timeout', 30)
        options.setdefault('vacuum', True)
        options.setdefault('thunder-lock', True)
        options.setdefault('log-x-forwarded-for', False)
        options.setdefault('buffer-size', 32768)
        options.setdefault('post-buffering', 65536)
        options.setdefault('limit-post', 20971520)
        options.setdefault('need-app', True)
        options.setdefault('disable-logging', False)
        options.setdefault('memory-report', True)
        options.setdefault('reload-on-rss', 600)
        options.setdefault('ignore-sigpipe', True)
        options.setdefault('ignore-write-errors', True)
        options.setdefault('disable-write-exception', True)
        options.setdefault('virtualenv', sys.prefix)
        options.setdefault('die-on-term', True)
        options.setdefault('log-format', '%(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size) "%(referer)" "%(uagent)"')

        options.setdefault('%s-socket' % options['protocol'], '%s:%s' % (host, port))

        # We only need to set uid/gid when stepping down from root, but if we are trying to run as root, then ignore it
        # entirely.
        uid = os.getuid()
        if uid > 0:
            options.setdefault('uid', uid)
        gid = os.getgid()
        if gid > 0:
            options.setdefault('gid', gid)

        # Required arguments that should not be overridden
        options['master'] = True
        options['enable-threads'] = True
        options['lazy-apps'] = True
        options['single-interpreter'] = True

        if workers:
            options['workers'] = workers

        self.options = options

    def prepare_environment(self, env=None):
        if env is None:
            env = os.environ

        # Move all of the options into UWSGI_ env vars
        for k, v in convert_options_to_env(self.options):
            env.setdefault(k, v)

        # Signal that we're running within uwsgi
        env['<% project_name|upper %>_RUNNING_UWSGI'] = '1'

        # This has already been validated inside __init__
        env['<% project_name|upper %>_SKIP_BACKEND_VALIDATION'] = '1'

        # Look up the bin directory where `<% project_name %>` exists, which should be
        # sys.argv[0], then inject that to the front of our PATH so we can reliably
        # find the `uwsgi` that's installed when inside virtualenv.
        # This is so the virtualenv doesn't need to be sourced in, which effectively
        # does exactly this.
        virtualenv_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        current_path = env.get('PATH', '')
        if virtualenv_path not in current_path:
            env['PATH'] = '%s:%s' % (virtualenv_path, current_path)

    def run(self):
        self.prepare_environment()
        os.execvp('uwsgi', ('uwsgi',))
