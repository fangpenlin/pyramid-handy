from __future__ import unicode_literals

import pytest

from . import make_app


@pytest.fixture
def testapp(settings=None):
    return make_app(
        'pyramid_handy.tweens.allow_origin_tween_factory',
        settings=settings,
    )


@pytest.fixture(params=[
    ['http://127.0.0.1', 'http://localhost'],
    # ensure newline splitted allowed_origins also work
    '\n'.join(['http://127.0.0.1', 'http://localhost']),
])
def allowed_origins(request):
    return request.param


@pytest.mark.parametrize('origin', [
    'http://127.0.0.1',
    'http://127.0.0.1/',
    'http://127.0.0.1/foo',
    'http://127.0.0.1/foo/bar',
    'http://127.0.0.1:6060/foo/bar',
    'http://localhost/',
    'http://localhost:5050/',
    'http://localhost/foo',
    'http://localhost/foo/bar',
])
def test_allowed(testapp, allowed_origins, origin):
    testapp.app.registry.settings['api.allowed_origins'] = allowed_origins
    origin = str(origin)
    resp = testapp.options(
        '/',
        headers={
            'Origin': origin,
        },
        status='*',
    )
    assert (
        resp.headers.get('Access-Control-Allow-Origin') == origin
    )
    assert (
        resp.headers.get('Access-Control-Allow-Credentials') == 'true'
    )
    assert (
        resp.headers.get('Access-Control-Allow-Methods') ==
        'GET, POST, PUT, DELETE, PATCH, OPTIONS',
    )
    assert (
        resp.headers.get('Access-Control-Allow-Headers') ==
        'Content-Type, Authorization, Range',
    )


@pytest.mark.parametrize('origin', [
    'http://127.0.0.2',
    'http://127.0.0.2/',
    'http://127.0.0.2/foo',
    'http://127.0.0.2/foo/bar',
    'http://my-localhost/',
    'http://my-localhost/foo',
    'http://my-localhost/foo/bar',
])
def test_not_allowed(testapp, allowed_origins, origin):
    testapp.app.registry.settings['api.allowed_origins'] = allowed_origins
    # ensure it works first
    resp = testapp.options(
        '/',
        headers={
            'Origin': b'http://127.0.0.1',
        },
        status='*',
    )
    resp_allow_origin = resp.headers.get('Access-Control-Allow-Origin', [])
    assert b'http://127.0.0.1' in resp_allow_origin
    # ensure given origin is not allowed
    origin = str(origin)
    resp = testapp.options(
        '/',
        headers={
            'Origin': origin,
        },
        status='*',
    )
    resp_allow_origin = resp.headers.get('Access-Control-Allow-Origin', [])
    assert origin not in resp_allow_origin


def test_function_settings(testapp):
    methods = 'YO, WHATSUP'
    headers = 'What-The-Fuck,X-Awesome'
    credentials = 'false'
    testapp.app.registry.settings.update({
        'api.allowed_origins': 'http://127.0.0.1',
        'api.allowed_methods': lambda request: methods,
        'api.allowed_headers': lambda request: headers,
        'api.allowed_credentials': lambda request: credentials,
    })
    resp = testapp.options(
        '/',
        headers={
            'Origin': b'http://127.0.0.1',
        },
        status='*',
    )
    assert (
        resp.headers.get('Access-Control-Allow-Credentials') == credentials
    )
    assert (
        resp.headers.get('Access-Control-Allow-Methods') == methods
    )
    assert (
        resp.headers.get('Access-Control-Allow-Headers') == headers
    )
