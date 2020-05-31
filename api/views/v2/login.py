import jwt
import logging
import json
from django.conf import settings
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('api')


class login(views.APIView):

    def post(self, request, *args, **kwargs):
        log_params = {}
        try:
            user = authenticate(
                request,
                username=request.data.get('username', None),
                password=request.data.get('password', None),
            )
            if user is None or not user.is_active:
                raise ValueError(_('there is no vaild user, please check'))

            encoded_data = jwt.encode({'user_id': user.id},
                                      settings.SECRET_KEY,
                                      algorithm='HS256')
        except:
            raise

        resp = {'token': str(encoded_data, 'utf-8')}

        log_params.update({
            'response': resp,
        })

        logger.info(json.dumps(log_params))

        return Response(resp, status=status.HTTP_200_OK)
