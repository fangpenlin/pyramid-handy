from __future__ import unicode_literals
import base64

import pytest

from . import make_app


def make_auth(username, password):
    encoded = base64.b64encode('{}:{}'.format(username, password))
    auth = b'basic {}'.format(encoded)
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
    (b'basic {}'.format(base64.b64encode('USERNAME')), None),
    (b'basic Breaking####Bad', None),
    (b'basic', None),
    (b'foobar', None),
    (b'foobar XXX', None),
    (None, None),
])
def test_basic_auth(testapp, auth, expected):
    kwargs = {}
    if auth is not None:
        kwargs['headers'] = dict(authorization=auth)
    resp = testapp.get(
        '/',
        status='*',
        **kwargs
    )
    assert resp.request.remote_user == expected
