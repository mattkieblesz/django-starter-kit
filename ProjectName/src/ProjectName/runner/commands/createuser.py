import click
from <% project_name %>.runner.decorators import configuration


def _get_field(field_name):
    from <% project_name %>.models import User
    return User._meta.get_field(field_name)


def _get_char_field(field_name):
    from django.core.exceptions import ValidationError
    rv = click.prompt(field_name.replace('_', ' ').capitalize())
    field = _get_field(field_name)
    try:
        return field.clean(rv, None)
    except ValidationError as e:
        raise click.ClickException('; '.join(e.messages))


def _get_password():
    from django.core.exceptions import ValidationError
    rv = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    field = _get_field('password')
    try:
        return field.clean(rv, None)
    except ValidationError as e:
        raise click.ClickException('; '.join(e.messages))


@click.command()
@click.option('--username')
@click.option('--email')
@click.option('--firstname')
@click.option('--lastname')
@click.option('--password')
@click.option('--superuser/--no-superuser', default=None, is_flag=True)
@click.option('--no-password', default=False, is_flag=True)
@click.option('--no-input', default=False, is_flag=True)
@configuration
def createuser(username, email, firstname, lastname, password, superuser, no_password, no_input):
    '''Create a new user.'''
    if not no_input:
        if not username:
            username = _get_char_field('username')

        if not email:
            email = _get_char_field('email')

        if not firstname:
            firstname = _get_char_field('first_name')

        if not lastname:
            lastname = _get_char_field('last_name')

        if not (password or no_password):
            password = _get_password()

        if superuser is None:
            superuser = click.confirm('Should this user be a superuser?', default=False)

    if superuser is None:
        superuser = False

    if not email:
        raise click.ClickException('Invalid or missing email address.')

    if not no_password and not password:
        raise click.ClickException('No password set and --no-password not passed.')

    from <% project_name %>.models import User

    user = User(
        username=username,
        email=email,
        first_name=firstname,
        last_name=lastname,
        is_superuser=superuser,
        is_staff=superuser,
        is_active=True,
    )

    if password:
        user.set_password(password)

    user.save()

    click.echo('User created: %s' % (email,))
