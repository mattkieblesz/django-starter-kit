import click
import os
import sys

import <% project_name %>
from <% project_name %>.utils.imports import import_string


# Parse out a pretty version for use with --version
if <% project_name %>.__build__ is None:
    version_string = <% project_name %>.VERSION
else:
    version_string = '%s (%s)' % (<% project_name %>.VERSION, <% project_name %>.__build__[:12])


@click.group()
@click.option('--config', default='', envvar='<% project_name|upper %>_CONF', help='Path to configuration files.', metavar='PATH')
@click.version_option(version=version_string)
@click.pass_context
def cli(ctx, config):
    '''
    Collaboration platform.

    The configuration file is looked up in the `~/.<% project_name %>` config directory but this can be overridden with the
    `<% project_name|upper %>_CONF` environment variable or be explicitly provided through the `--config` parameter.
    '''
    from .settings import DEFAULT_CONFIG_DIR
    if config:
        os.environ['<% project_name|upper %>_CONF'] = config
    os.environ.setdefault('<% project_name|upper %>_CONF', DEFAULT_CONFIG_DIR)


list(map(lambda cmd: cli.add_command(import_string(cmd)), (
    '<% project_name %>.runner.commands.createuser.createuser',
    '<% project_name %>.runner.commands.django.django',
    '<% project_name %>.runner.commands.init.init',
    '<% project_name %>.runner.commands.initdata.initdata',
    '<% project_name %>.runner.commands.run.run',
    '<% project_name %>.runner.commands.upgrade.upgrade',
)))


def configure():
    from .settings import discover_configs, configure
    try:
        ctx = click.get_current_context()
    except RuntimeError:
        ctx = None
    _, py = discover_configs()

    configure(ctx, py)


def get_prog():
    '''
    Extract the proper program executable.

    In the case of `python -m <% project_name %>`, we want to detect this and make sure we return something useful rather than
    __main__.py
    '''
    try:
        if os.path.basename(sys.argv[0]) in ('__main__.py', '-c'):
            return '%s -m <% project_name %>' % sys.executable
    except (AttributeError, TypeError, IndexError):
        pass
    return '<% project_name %>'


class UnknownCommand(ImportError):
    pass


def call_command(name, obj=None, **kwargs):
    try:
        command = import_string(name)
    except (ImportError, AttributeError):
        raise UnknownCommand(name)

    with command.make_context('<% project_name %>', [], obj=obj or {}) as ctx:
        ctx.params.update(kwargs)
        try:
            command.invoke(ctx)
        except click.Abort:
            click.echo('Aborted!', err=True)


def main():
    cli(prog_name=get_prog(), obj={}, max_content_width=100)
