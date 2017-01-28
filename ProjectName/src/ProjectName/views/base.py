from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View

from <% project_name %>.utils import auth


class BaseView(View):
    auth_required = True
    sudo_required = False

    def __init__(self, auth_required=None, sudo_required=None, *args, **kwargs):
        if auth_required is not None:
            self.auth_required = auth_required
        if sudo_required is not None:
            self.sudo_required = sudo_required
        super(BaseView, self).__init__(*args, **kwargs)

    def convert_args(self, request, *args, **kwargs):
        return (args, kwargs)

    def get_context_data(self, request, **kwargs):
        return csrf(request)

    def is_auth_required(self, request, *args, **kwargs):
        return (
            self.auth_required
            and not (request.user.is_authenticated() and request.user.is_active)
        )

    def handle_auth_required(self, request, *args, **kwargs):
        return self.redirect(auth.get_login_url())

    def has_permission(self, request, *args, **kwargs):
        return True

    def handle_permission_required(self, request, *args, **kwargs):
        redirect_uri = self.get_no_permission_url(request, *args, **kwargs)
        return self.redirect(redirect_uri)

    def get_no_permission_url(request, *args, **kwargs):
        return auth.get_login_url()

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if self.is_auth_required(request, *args, **kwargs):
            return self.handle_auth_required(request, *args, **kwargs)

        args, kwargs = self.convert_args(request, *args, **kwargs)

        if not self.has_permission(request, *args, **kwargs):
            return self.handle_permission_required(request, *args, **kwargs)

        self.request = request
        self.default_context = self.get_context_data(request, *args, **kwargs)

        return self.handle(request, *args, **kwargs)

    def handle(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)

    def respond(self, template, context=None, status=200, content_type='text/html'):
        default_context = self.default_context
        if context:
            default_context.update(context)

        context = default_context

        return render(self.request, template, context, content_type, status)

    def redirect(self, url):
        return HttpResponseRedirect(url)
