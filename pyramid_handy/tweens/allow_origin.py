from __future__ import unicode_literals


def allow_origin_tween_factory(handler, registry):
    """Allow cross origin XHR requests

    """
    def allow_origin_tween(request):
        settings = request.registry.settings
        request_origin = request.headers.get('origin')

        def is_origin_allowed(origin):
            allowed_origins = (
                request.registry.settings.get('api.allowed_origins', [])
            )
            if isinstance(allowed_origins, (str, unicode)):
                allowed_origins = allowed_origins.splitlines()
            if not origin:
                return False
            for allowed_origin in allowed_origins:
                if origin.lower().startswith(allowed_origin):
                    return True
            return False

        def allow_origin_callback(request, response):
            """Set access-control-allow-origin et. al headers

            """
            allowed_methods = settings.get(
                'api.allowed_methods',
                b'GET, POST, PUT, DELETE, PATCH, OPTIONS',
            )
            if callable(allowed_methods):
                allowed_methods = allowed_methods(request)

            allowed_headers = settings.get(
                'api.allowed_headers',
                b'Content-Type, Authorization, Range',
            )
            if callable(allowed_headers):
                allowed_headers = allowed_headers(request)

            allowed_credentials = settings.get(
                'api.allowed_credentials',
                b'true',
            )
            if callable(allowed_credentials):
                allowed_credentials = allowed_credentials(request)

            response.headers[b'Access-Control-Allow-Origin'] = request_origin
            if allowed_credentials:
                response.headers[b'Access-Control-Allow-Credentials'] = str(
                    allowed_credentials,
                )
            if allowed_methods:
                response.headers[b'Access-Control-Allow-Methods'] = str(
                    allowed_methods,
                )
            if allowed_headers:
                response.headers[b'Access-Control-Allow-Headers'] = str(
                    allowed_headers,
                )

        if not is_origin_allowed(request_origin):
            return handler(request)

        request.add_response_callback(allow_origin_callback)
        return handler(request)
    return allow_origin_tween
