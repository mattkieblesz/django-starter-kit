import click
from <% project_name %>.runner.decorators import configuration


@click.command()
@click.option('--verbosity', '-v', default=1, help='Verbosity level.')
@click.option('--traceback', default=True, is_flag=True, help='Raise on exception.')
@click.option('--noinput', default=False, is_flag=True, help='Do not prompt the user for input of any kind.')
@configuration
@click.pass_context
def upgrade(ctx, verbosity, traceback, noinput):
    '''Perform any pending database migrations and upgrades.'''
    from django.core.management import call_command as dj_call_command

    dj_call_command(
        'migrate',
        merge=True,
        interactive=not noinput,
        traceback=traceback,
        verbosity=verbosity,
    )
