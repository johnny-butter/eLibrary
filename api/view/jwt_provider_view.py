import jwt
from django.conf import settings
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class jwtProvider(views.APIView):

    def post(self, request, *args, **kwargs):
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

        return Response({'token': encoded_data}, status=status.HTTP_200_OK)
