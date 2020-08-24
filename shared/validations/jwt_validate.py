import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status, HTTP_HEADER_ENCODING, authentication
from rest_framework.response import Response
from shared.error_code import AuthenticationFailed, InvalidToken


AUTH_HEADER_TYPES = ['Bearer', 'JWT']

AUTH_HEADER_TYPE_BYTES = set(
    header_type.encode(HTTP_HEADER_ENCODING)
    for header_type in AUTH_HEADER_TYPES
)


class JWTAuthentication(authentication.BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), None

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get('HTTP_AUTHORIZATION')

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                detail=_(
                    'Authorization header must contain two space-delimited values'),
                code='bad_authorization_header',
            )

        return parts[1]

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        try:
            return jwt.decode(raw_token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            raise InvalidToken(
                detail=_('Given token not valid for any token type'))

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken(
                detail=_('Token contained no recognizable user identification'))

        try:
            User = get_user_model()
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(
                detail=_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(
                detail=_('User is inactive'), code='user_inactive')

        return user
