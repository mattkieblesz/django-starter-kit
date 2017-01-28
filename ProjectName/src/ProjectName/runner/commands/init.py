import os
import click


@click.command()
@click.option('--dev', default=False, is_flag=True, help='Use settings more conducive to local development.')
@click.argument('directory', required=False)
@click.pass_context
def init(ctx, dev, directory):
    '''Initialize new configuration directory.'''
    from <% project_name %>.runner.settings import discover_configs, generate_settings
    if directory is not None:
        os.environ['<% project_name|upper %>_CONF'] = directory

    directory, py = discover_configs()

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(py):
        click.confirm("File already exists at '%s', overwrite?" % click.format_filename(py), abort=True)

    with click.open_file(py, 'w') as fp:
        config_contents = generate_settings(dev)
        fp.write(config_contents)
