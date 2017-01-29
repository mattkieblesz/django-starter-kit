import click
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from <% project_name %>.runner.decorators import configuration


@click.command()
@configuration
def initdata():
    '''Populate database with initial data.'''
    from django.contrib.sites.models import Site
    from <% project_name %>.models import User
    from <% project_name %>.runner import call_command

    # if command was run already skip
    if User.objects.count() > 0:
        return

    if not click.confirm('\nWould you like to populate database with initial data?', default=True):
        click.echo('\nRun `<% project_name %> initdata` to do this later.\n')
        return

    site = Site.objects.get_current()
    site.domain = settings.SITE_DOMAIN
    site.name = settings.SITE_NAME
    site.save()

    # initial users
    User.objects.create_user('root', settings.SERVER_EMAIL, first_name='<% project_title %>')
    click.echo('\nCreate superuser:')
    # populate for testing initially
    call_command(
        '<% project_name %>.runner.commands.createuser.createuser',
        username='<% first_name|lower %>',
        email='<% first_name|lower %>@<% email_domain %>',
        firstname='<% first_name %>',
        lastname='<% last_name %>',
        password='test',
        superuser=True
    )
    super_user = User.objects.latest('date_joined')

    click.echo('Database populated')
