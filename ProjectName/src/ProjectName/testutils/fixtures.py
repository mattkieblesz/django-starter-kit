from exam import fixture
from uuid import uuid4


class Fixtures(object):
    @fixture
    def user(self):
        return self.create_user('admin@localhost', is_superuser=True)

    def create_user(self, email=None, **kwargs):
        from <% project_name %>.models import User

        if not email:
            email = uuid4().hex + '@example.com'

        kwargs.setdefault('username', email)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', False)

        user = User(email=email, **kwargs)
        user.set_password('admin')
        user.save()

        return user
