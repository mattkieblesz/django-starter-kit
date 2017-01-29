import os

from click import Choice

LOG_LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'FATAL')


class CaseInsensitiveChoice(Choice):
    def convert(self, value, param, ctx):
        self.choices = [choice.upper() for choice in self.choices]
        return super(CaseInsensitiveChoice, self).convert(value.upper(), param, ctx)


def configuration(f):
    "Load and configure <% project_title %>."
    import click
    from functools import update_wrapper

    @click.pass_context
    def inner(ctx, *args, **kwargs):
        # HACK: We can't call `configure()` from within tests since we don't load config files from disk, so we need a
        # way to bypass this initialization step
        if os.environ.get('_<% project_name|upper %>_SKIP_CONFIGURATION') != '1':
            from <% project_name %>.runner import configure
            configure()
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(inner, f)


def log_options(default=None):
    def decorator(f):
        '''Give ability to configure global logging level/format. Must be used before configuration.'''
        import click
        from functools import update_wrapper

        @click.pass_context
        @click.option('--loglevel', '-l', default=default,
            help='Global logging level. Use wisely.',
            envvar='<% project_name|upper %>_LOG_LEVEL',
            type=CaseInsensitiveChoice(LOG_LEVELS))
        def inner(ctx, loglevel=None, *args, **kwargs):
            if loglevel:
                os.environ['<% project_name|upper %>_LOG_LEVEL'] = loglevel
            return ctx.invoke(f, *args, **kwargs)
        return update_wrapper(inner, f)
    return decorator
