from __future__ import unicode_literals


def api_headers_tween_factory(handler, registry):
    """This tween provides necessary API headers

    """
    def api_headers_tween(request):
        return handler(request)
    return api_headers_tween
