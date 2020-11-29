import json
import logging
from rest_framework.response import Response


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

        if response['Content-Type'] == 'application/json' and isinstance(response, Response):
            log_data = {k: v for k, v in request.META.items() if k.startswith('HTTP_')}
            log_data.update(response.data)

            self.logger.info(json.dumps(log_data))

        return response
