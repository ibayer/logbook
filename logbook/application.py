from werkzeug.wrappers import Request
from werkzeug.wsgi import ClosingIterator, SharedDataMiddleware
from werkzeug.exceptions import HTTPException, NotFound
from logbook.utils import STATIC_PATH, url_map, local, local_manager


import logbook.models
from logbook import views


class Logbook(object):

    def __init__(self):
        local.application = self

        self.dispatch = SharedDataMiddleware(self.dispatch, {
            '/static':  STATIC_PATH
        })

    def dispatch(self, environ, start_response):
        local.application = self
        request = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except NotFound, e:
            response = views.not_found(request)
            response.status_code = 404
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response),
                               [local_manager.cleanup])

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)
