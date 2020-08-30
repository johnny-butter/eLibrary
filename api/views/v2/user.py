from api.models import User
from api.serializers import UserSerializer
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        elif view.action in ['retrieve', 'partial_update']:
            return request.user.is_authenticated

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['retrieve', 'partial_update']:
            return obj == request.user

        return False


class User(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
           mixins.DestroyModelMixin, GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        if request.data.get('oauth_record', {}).get('provider', None):
            data.update({
                'username': User.random_username(),
                'password': User.random_password(),
            })

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
