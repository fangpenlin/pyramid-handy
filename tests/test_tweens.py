from __future__ import unicode_literals
import base64

import pytest
import webtest
from pyramid.config import Configurator

import pyramid_handy


def make_app(tween_factory, settings=None):
    settings = settings or {}
    config = Configurator(settings=settings)
    config.add_tween(
        tween_factory,
    )
    app = config.make_wsgi_app()
    testapp = webtest.TestApp(app)
    return testapp


@pytest.fixture
def api_header_app(settings=None):
    return make_app('pyramid_handy.tweens.api_headers_tween_factory')


def test_header_version_and_revision(api_header_app):
    version_header = 'X-Core-Version'
    revision_header = 'X-Core-Revision'
    self.settings.update({
        'api.version_header': version_header,
        'api.version_header_value': 'pyramid_handy:__version__',
        'api.revision_header': revision_header,
        'api.revision_header_value': 'pyramid_handy:__git_revision__',
    })
    resp = self.testapp.get('/', status='*')
    self.assertEqual(resp.headers[version_header], pyramid_handy.__version__)
    self.assertEqual(resp.headers[revision_header], pyramid_handy.__git_revision__)

def test_header_version_and_revision_callable(self):
    self.settings.update({
        'api.version_header_value': lambda: 'foo',
        'api.revision_header_value': lambda: 'bar',
    })
    resp = self.testapp.get('/', status='*')
    self.assertEqual(resp.headers['X-Version'], 'foo')
    self.assertEqual(resp.headers['X-Revision'], 'bar')

def test_header_not_present(self):
    self.settings.update({
        'api.version_header_value': None,
        'api.revision_header_value': None,
    })
    resp = self.testapp.get('/', status='*')
    self.assertNotIn('X-Version', resp.headers)
    self.assertNotIn('X-Revision', resp.headers)

def test_req_guid_header(self):
    self.settings.update()
    resp = self.testapp.get('/', status='*')
    self.assertIn('X-Req-Guid', resp.headers)

def test_req_guid_header_not_present(self):
    self.settings.update({
        'api.req_guid_header': None,
    })
    resp = self.testapp.get('/', status='*')
    self.assertNotIn('X-Req-Guid', resp.headers)


class TestAllowOriginTween(BasicTweenTest):

    tween_factory = 'pyramid_handy.tweens.allow_origin_tween_factory'

    def assert_allowed(self, origin):
        origin = str(origin)
        resp = self.testapp.options(
            '/',
            headers={
                'Origin': origin,
            },
            status='*',
        )
        self.assertEqual(
            resp.headers.get('Access-Control-Allow-Origin'),
            origin,
        )
        self.assertEqual(
            resp.headers.get('Access-Control-Allow-Credentials'),
            'true',
        )
        self.assertEqual(
            resp.headers.get('Access-Control-Allow-Methods'),
            'GET, POST, PUT, DELETE, PATCH, OPTIONS',
        )
        self.assertEqual(
            resp.headers.get('Access-Control-Allow-Headers'),
            'Content-Type, Authorization, Range',
        )

    def assert_not_allowed(self, origin):
        origin = str(origin)
        resp = self.testapp.options(
            '/',
            headers={
                'Origin': origin,
            },
            status='*',
        )
        resp_allow_origin = resp.headers.get('Access-Control-Allow-Origin', [])
        self.assertNotIn(origin, resp_allow_origin)

    def test_allow_origin(self):
        self.settings['api.allowed_origins'] = [
            'http://127.0.0.1',
            'http://localhost',
        ]
        self.assert_allowed('http://127.0.0.1')
        self.assert_allowed('http://127.0.0.1/')
        self.assert_allowed('http://127.0.0.1/foo')
        self.assert_allowed('http://127.0.0.1/foo/bar')
        self.assert_allowed('http://127.0.0.1:6060/foo/bar')
        self.assert_allowed('http://localhost/')
        self.assert_allowed('http://localhost:5050/')
        self.assert_allowed('http://localhost/foo')
        self.assert_allowed('http://localhost/foo/bar')

    def test_allow_origin_with_multiiple_line_cfg(self):
        self.settings['api.allowed_origins'] = '\n'.join([
            'http://127.0.0.1',
            'http://localhost',
        ])
        self.assert_allowed('http://127.0.0.1')
        self.assert_allowed('http://localhost/')

    def test_not_allow_origin(self):
        self.settings['api.allowed_origins'] = [
            'http://127.0.0.1',
            'http://localhost',
        ]
        self.assert_not_allowed('http://127.0.0.2')
        self.assert_not_allowed('http://127.0.0.2/')
        self.assert_not_allowed('http://127.0.0.2/foo')
        self.assert_not_allowed('http://127.0.0.2/foo/bar')
        self.assert_not_allowed('http://my-localhost/')
        self.assert_not_allowed('http://my-localhost/foo')
        self.assert_not_allowed('http://my-localhost/foo/bar')

    def test_function_settings(self):
        methods = 'YO, WHATSUP'
        headers = 'What-The-Fuck,X-Awesome'
        credentials = 'false'
        self.settings.update({
            'api.allowed_origins': 'http://127.0.0.1',
            'api.allowed_methods': lambda request: methods,
            'api.allowed_headers': lambda request: headers,
            'api.allowed_credentials': lambda request: credentials,
        })
        resp = self.testapp.options(
            '/',
            headers={
                'Origin': b'http://127.0.0.1',
            },
            status='*',
        )
        self.assertEqual(
            resp.headers.get('Access-Control-Allow-Credentials'),
            credentials,
        )
        self.assertEqual(
            resp.headers.get('Access-Control-Allow-Methods'),
            methods,
        )
        self.assertEqual(
            resp.headers.get('Access-Control-Allow-Headers'),
            headers,
        )


class TestBasicAuthTween(BasicTweenTest):

    tween_factory = 'pyramid_handy.tweens.basic_auth_tween_factory'

    def make_auth(self, username, password):
        encoded = base64.b64encode('{}:{}'.format(username, password))
        auth = b'basic {}'.format(encoded)
        return auth

    def assert_remote_user(self, auth, exepcted):
        resp = self.testapp.get(
            '/',
            headers=dict(authorization=auth),
            status='*',
        )
        self.assertEqual(resp.request.remote_user, exepcted)

    def test_remote_user(self):
        auth = self.make_auth('USERNAME', 'PASSWORD')
        self.assert_remote_user(auth, 'USERNAME')

    def test_auth_without_base64_part(self):
        encoded = base64.b64encode('USERNAME')
        auth = b'basic {}'.format(encoded)
        self.assert_remote_user(auth, None)

    def test_auth_with_bad_base64(self):
        self.assert_remote_user(b'basic Breaking####Bad', None)

    def test_auth_without_colon(self):
        self.assert_remote_user(b'basic', None)

    def test_auth_non_basic(self):
        self.assert_remote_user(b'foobar XXX', None)

    def test_without_auth_header(self):
        resp = self.testapp.get(
            '/',
            status='*',
        )
        self.assertEqual(resp.request.remote_user, None)
