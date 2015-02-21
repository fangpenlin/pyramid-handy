from __future__ import unicode_literals


def allow_origin_tween_factory(handler, registry):
    """Allow cross origin XHR requests

    """
    def allow_origin_tween(request):
        return handler(request)
    return allow_origin_tween
