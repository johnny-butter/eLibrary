import json
import logging


class ApiLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('api')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        #  NOTE: use "data" attribute to distinguish api response
        if hasattr(response, 'data'):
            headers = {k: v for k, v in request.META.items() if k.startswith('HTTP_')}
            self.logger.info(json.dumps(headers))
            self.logger.info(json.dumps(response.data))

        return response
