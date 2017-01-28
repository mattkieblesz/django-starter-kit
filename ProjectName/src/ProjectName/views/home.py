from <% project_name %>.views.base import BaseView


class Home(BaseView):
    auth_required = False

    def get(self, request):
        return self.respond('<% project_name %>/home.html')
