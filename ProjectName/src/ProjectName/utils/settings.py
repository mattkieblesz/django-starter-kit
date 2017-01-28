import inspect
import sys

PACKAGES = {
    'django.db.backends.postgresql_psycopg2': 'psycopg2.extensions',
    'django.core.cache.backends.memcached.MemcachedCache': 'memcache',
}


def reraise(tp, value, tb=None):
    '''Imported from six'''
    if value is None:
        value = tp()
    if value.__traceback__ is not tb:
        raise value.with_traceback(tb)
    raise value


def reraise_as(new_exception_or_type):
    '''
    Obtained from https://github.com/dcramer/reraise/blob/master/src/reraise.py
    >>> try:
    >>>     do_something_crazy()
    >>> except Exception:
    >>>     reraise_as(UnhandledException)
    '''
    __traceback_hide__ = True  # NOQA

    e_type, e_value, e_traceback = sys.exc_info()

    if inspect.isclass(new_exception_or_type):
        new_type = new_exception_or_type
        new_exception = new_exception_or_type()
    else:
        new_type = type(new_exception_or_type)
        new_exception = new_exception_or_type

    new_exception.__cause__ = e_value

    try:
        reraise(new_type, new_exception, e_traceback)
    finally:
        del e_traceback
