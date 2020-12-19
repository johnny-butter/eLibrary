import jwt

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import status, views
from rest_framework.response import Response

from shared.errors import AuthenticationFailed


class Login(views.APIView):

    def post(self, request, *args, **kwargs):
        try:
            user = authenticate(
                request,
                username=request.data.get('username', None),
                password=request.data.get('password', None),
            )
            if user is None or not user.is_active:
                raise AuthenticationFailed(detail=_('User not found'))

            encoded_data = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, algorithm='HS256')
        except Exception:
            raise

        resp = {'token': str(encoded_data, 'utf-8')}

        return Response(resp, status=status.HTTP_200_OK)
