from rest_framework import status
from rest_framework.response import Response
from api.serializers import bookFavSerializer, bookFavGetSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated


class favBook(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == 'GET':

            queryset = self.request.user.favoritebook_set.select_related(
                'book').select_related('book__author').select_related('book__type').favorited()

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = bookFavGetSerializer
        elif self.request.method == 'POST':
            serializer_class = bookFavSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        resp = {
            'username': self.request.user.username,
            'data': serializer.data,
        }

        return Response(resp, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
