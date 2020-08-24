import jwt
from channels.sessions import CookieMiddleware, SessionMiddleware
from channels.auth import AuthMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from shared.error_code import AuthenticationFailed, InvalidToken


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        raw_token = scope['cookies'].get('token', None)

        if raw_token:
            validated_token = jwt.decode(
                raw_token, settings.SECRET_KEY, algorithms=['HS256'])

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

            scope['user'] = user

        return self.inner(scope)


def JWTAuthMiddlewareStack(inner):
    return CookieMiddleware(
        JWTAuthMiddleware(
            SessionMiddleware(
                AuthMiddleware(inner)
            )
        )
    )
