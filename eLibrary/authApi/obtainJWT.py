from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase
from django.contrib.auth.backends import ModelBackend, UserModel


class emailOrUsernameJWTSerializer(TokenObtainSerializer):

    def validate(self, attrs):
        if '@' in attrs[self.username_field]:
            attrs['email'] = attrs[self.username_field]
            self.username_field = 'email'
        return super().validate(attrs)


class obtainJWTTokenPairSerializer(TokenObtainPairSerializer, emailOrUsernameJWTSerializer):

    def validate(self, attrs):
        print(self.__class__.mro())
        data = super().validate(attrs)
        return data


class obtainJWTTokenPairView(TokenViewBase):

    serializer_class = obtainJWTTokenPairSerializer


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
