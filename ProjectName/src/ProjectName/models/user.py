from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from <% project_name %>.db.models import BaseModel


class UserManager(UserManager):
    pass


class User(BaseModel, AbstractUser):
    pass

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        app_label = '<% project_name %>'
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def delete(self):
        if self.username == 'root':
            raise Exception('You cannot delete the "root" user as it is required by the app.')

        self.is_active = False
        return super().save()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        return super().save(*args, **kwargs)

    def get_label(self):
        return self.email or self.username or self.id

    def get_display_name(self):
        return self.email or self.username

    def get_short_name(self):
        return self.username
