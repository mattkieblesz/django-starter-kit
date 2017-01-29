import os
import os.path

from subprocess import check_output

try:
    VERSION = __import__('pkg_resources').get_distribution('<% project_name %>').version
except Exception:
    VERSION = 'unknown'


def _get_git_revision(path):
    if not os.path.exists(os.path.join(path, '.git')):
        return None
    try:
        revision = check_output(['git', 'rev-parse', 'HEAD'], cwd=path, env=os.environ)
    except Exception:
        return None
    return revision.strip()


def get_revision():
    if '<% project_name|upper %>_BUILD' in os.environ:
        return os.environ['<% project_name|upper %>_BUILD']
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, os.pardir, os.pardir))
    path = os.path.join(checkout_dir)
    if os.path.exists(path):
        return _get_git_revision(path)
    return None


def get_version():
    if __build__:
        return '%s.%s' % (__version__, __build__)
    return __version__


__version__ = VERSION
__build__ = get_revision()
