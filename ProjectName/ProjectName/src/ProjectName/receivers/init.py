from django.db.models.signals import post_migrate


def init_data(*args, **kwargs):
    # post migrate is run for all apps, run it only for <% project_name %> app
    if kwargs['app_config'].name != '<% project_name %>':
        return

    if not kwargs.get('interactive', True):
        return

    from <% project_name %>.runner import call_command
    call_command('<% project_name %>.runner.commands.initdata.initdata')


post_migrate.connect(init_data, dispatch_uid="init_data", weak=False)
