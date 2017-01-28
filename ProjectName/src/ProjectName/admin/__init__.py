from django.contrib import admin

from <% project_name %>.models import User
from .user import UserAdmin

admin.site.register(User, UserAdmin)
