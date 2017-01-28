import click

from <% project_name %>.runner.decorators import configuration, log_options


class AddressParamType(click.ParamType):
    name = 'address'

    def __call__(self, value, param=None, ctx=None):
        if value is None:
            return (None, None)
        return self.convert(value, param, ctx)

    def convert(self, value, param, ctx):
        if ':' in value:
            host, port = value.split(':', 1)
            port = int(port)
        else:
            host = value
            port = None
        return host, port


Address = AddressParamType()


@click.group()
def run():
    '''Run a service.'''


@run.command()
@click.option('--bind', '-b', default=None, help='Bind address.', type=Address)
@click.option('--workers', '-w', default=0, help='The number of worker processes for handling requests.')
@log_options()
@configuration
def web(bind, workers):
    'Run web service.'
    from <% project_name %>.services.http import HTTPServer
    HTTPServer(host=bind[0], port=bind[1], workers=workers).run()
