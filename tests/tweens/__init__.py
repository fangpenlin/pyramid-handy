from __future__ import unicode_literals

import webtest
from pyramid.config import Configurator


def make_app(tween_factory, settings=None):
    settings = settings or {}
    config = Configurator(settings=settings)
    config.add_tween(
        tween_factory,
    )
    app = config.make_wsgi_app()
    testapp = webtest.TestApp(app)
    return testapp
