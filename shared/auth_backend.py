from django.contrib.auth.backends import ModelBackend, UserModel
from api.models import oauthRecord


class emailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        identityKey = 'email' if '@' in username else 'username'

        try:
            user = UserModel._default_manager.get(**{identityKey: username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class oauthModelBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        provider = request.data.get('provider', None)
        uid = request.data.get('uid', None)

        if provider is None or uid is None:
            return

        try:
            user = oauthRecord.objects.get(provider=provider, uid=uid).user
        except oauthRecord.DoesNotExist:
            pass
        else:
            return user
