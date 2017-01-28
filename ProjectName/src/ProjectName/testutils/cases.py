import base64
import os
import os.path

from contextlib import contextmanager
from django.conf import settings
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase, TransactionTestCase
from importlib import import_module
from exam import before, Exam

from <% project_name %>.constants import MODULE_ROOT
from <% project_name %>.utils import json

from .fixtures import Fixtures

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'


class BaseTestCase(Fixtures, Exam):
    urls = '<% project_name %>.conf.urls'

    def assertRequiresAuthentication(self, path, method='GET'):
        resp = getattr(self.client, method.lower())(path)
        assert resp.status_code == 302
        assert resp['Location'].startswith('http://testserver' + reverse('<% project_name %>-login'))

    @before
    def setup_session(self):
        engine = import_module(settings.SESSION_ENGINE)

        session = engine.SessionStore()
        session.save()

        self.session = session

    def save_session(self):
        self.session.save()

        cookie_data = {
            'max-age': None,
            'path': '/',
            'domain': settings.SESSION_COOKIE_DOMAIN,
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'expires': None,
        }

        session_cookie = settings.SESSION_COOKIE_NAME
        self.client.cookies[session_cookie] = self.session.session_key
        self.client.cookies[session_cookie].update(cookie_data)

    def login_as(self, user, organization_id=None):
        user.backend = settings.AUTHENTICATION_BACKENDS[0]

        request = HttpRequest()
        request.session = self.session

        login(request, user)
        request.user = user

        # Save the session values.
        self.save_session()

    def load_fixture(self, filepath):
        filepath = os.path.join(
            MODULE_ROOT,
            'tests',
            'fixtures',
            filepath,
        )
        with open(filepath, 'rb') as fp:
            return fp.read()

    def _pre_setup(self):
        super(BaseTestCase, self)._pre_setup()

    def _post_teardown(self):
        super(BaseTestCase, self)._post_teardown()

    def _makeMessage(self, data):
        return json.dumps(data).encode('utf-8')

    def _makePostMessage(self, data):
        return base64.b64encode(self._makeMessage(data))

    @contextmanager
    def dsn(self, dsn):
        """
        A context manager that temporarily sets the internal client's DSN
        """
        from raven.contrib.django.models import client

        try:
            client.set_dsn(dsn)
            yield
        finally:
            client.set_dsn(None)


class TestCase(BaseTestCase, TestCase):
    pass


class TransactionTestCase(BaseTestCase, TransactionTestCase):
    pass
