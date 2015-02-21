from __future__ import unicode_literals

import pytest

from . import make_app

__version__ = '9.9.9'
__git_revision__ = 'asdf12345'


@pytest.fixture
def testapp(settings=None):
    return make_app(
        'pyramid_handy.tweens.api_headers_tween_factory',
        settings=settings,
    )


def test_header_version_and_revision(testapp):
    version_header = 'X-Core-Version'
    revision_header = 'X-Core-Revision'
    testapp.app.registry.settings.update({
        'api.version_header': version_header,
        'api.version_header_value': 'tests.tweens.test_api_headers:__version__',
        'api.revision_header': revision_header,
        'api.revision_header_value': (
            'tests.tweens.test_api_headers:__git_revision__'
        )
    })
    resp = testapp.get('/', status='*')
    assert resp.headers[version_header] == __version__
    assert resp.headers[revision_header] == __git_revision__


def test_header_version_and_revision_callable(testapp):
    testapp.app.registry.settings.update({
        'api.version_header_value': lambda: 'foo',
        'api.revision_header_value': lambda: 'bar',
    })
    resp = testapp.get('/', status='*')
    resp.headers['X-Version'] == 'foo'
    resp.headers['X-Revision'] == 'bar'


def test_header_not_present(testapp):
    testapp.app.registry.settings.update({
        'api.version_header_value': None,
        'api.revision_header_value': None,
    })
    resp = testapp.get('/', status='*')
    assert 'X-Version' not in resp.headers
    assert 'X-Revision' not in resp.headers


def test_req_guid_header(testapp):
    resp = testapp.get('/', status='*')
    assert 'X-Req-Guid' in resp.headers


def test_req_guid_header_not_present(testapp):
    testapp.app.registry.settings.update({
        'api.req_guid_header': None,
    })
    resp = testapp.get('/', status='*')
    assert 'X-Req-Guid' not in resp.headers
