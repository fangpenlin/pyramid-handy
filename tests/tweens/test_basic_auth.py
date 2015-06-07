from __future__ import unicode_literals

import base64

import pytest

from . import make_app


def make_auth(username, password):
    encoded = base64.b64encode(
        '{}:{}'.format(username, password).encode('utf8')
    )
    auth = 'basic {}'.format(encoded.decode('utf8'))
    return auth


@pytest.fixture
def testapp(settings=None):
    return make_app(
        'pyramid_handy.tweens.basic_auth_tween_factory',
        settings=settings,
    )


@pytest.mark.parametrize('auth, expected', [
    (make_auth('', 'PASSWORD'), ''),
    (make_auth('USERNAME', 'PASSWORD'), 'USERNAME'),
    (
        'basic {}'.format(base64.b64encode(b'USERNAME').decode('utf8')),
        None,
    ),
    ('basic Breaking####Bad', None),
    ('basic', None),
    ('foobar', None),
    ('foobar XXX', None),
    (None, None),
])
def test_basic_auth(testapp, auth, expected):
    kwargs = {}
    if auth is not None:
        kwargs['headers'] = dict(authorization=str(auth))
    resp = testapp.get(
        '/',
        status='*',
        **kwargs
    )
    assert resp.request.remote_user == expected
