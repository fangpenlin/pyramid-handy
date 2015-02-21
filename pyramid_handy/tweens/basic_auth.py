from __future__ import unicode_literals


def basic_auth_tween_factory(handler, registry):
    """Do basic authentication, parse HTTP_AUTHORIZATION and set remote_user
    variable to request

    """
    def basic_auth_tween(request):
        return handler(request)
    return basic_auth_tween
