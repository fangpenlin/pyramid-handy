from __future__ import unicode_literals
import uuid

from pyramid.path import DottedNameResolver


def set_version(request, response):
    """Set version and revision to response

    """
    settings = request.registry.settings
    resolver = DottedNameResolver()

    # get version config
    version_header = settings.get(
        'api.version_header',
        'X-Version',
    )
    version_header_value = settings.get('api.version_header_value')
    if callable(version_header_value):
        version_header_value = version_header_value()
    elif version_header_value:
        version_header_value = resolver.resolve(version_header_value)

    # get revision config
    revision_header = settings.get(
        'api.revision_header',
        'X-Revision',
    )
    revision_header_value = settings.get('api.revision_header_value')
    if callable(revision_header_value):
        revision_header_value = revision_header_value()
    elif revision_header_value:
        revision_header_value = resolver.resolve(revision_header_value)

    if version_header and version_header_value:
        response.headers[str(version_header)] = str(version_header_value)
    if revision_header and revision_header_value:
        response.headers[str(revision_header)] = str(revision_header_value)


def set_req_guid(request, response):
    settings = request.registry.settings
    # get revision config
    req_guid_header = settings.get(
        'api.req_guid_header',
        'X-Req-Guid',
    )
    if not req_guid_header:
        return

    # TODO: what about security issue? what about attacker feeds us a
    # mal-format req_guid or what? a hash signed guid instead?
    req_guid = request.headers.get(req_guid_header)
    if req_guid is None:
        req_guid = uuid.uuid4().hex
    if not req_guid:
        return
    response.headers[str(req_guid_header)] = str(req_guid)


def api_headers_tween_factory(handler, registry):
    """This tween provides necessary API headers

    """

    def api_headers_tween(request):
        response = handler(request)
        set_version(request, response)
        set_req_guid(request, response)
        return response

    return api_headers_tween
