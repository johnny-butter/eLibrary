from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Book, favoriteBook
from .serializers import userSerializer, bookSerializer, bookFavSerializer, bookFavGetSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from jsonreader import JsonReader
# from .voter import userVoter
import urllib
import requests
import json
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.exceptions import AuthenticationFailed


class bookPaging(PageNumberPagination):
    def get_paginated_response(self, data):
        nowPage = int(self.request.query_params.get(self.page_query_param, 1))
        return Response({'total_page': self.page.paginator.num_pages,
                         'current_page': nowPage,
                         'has_previous': self.page.has_previous(),
                         'has_next': self.page.has_next(),
                         'data': data})


class getUserList(mixins.CreateModelMixin, GenericViewSet):
    # queryset = User.objects.all()
    serializer_class = userSerializer


class getUserDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer

    def retrieve(self, request, *args, **kwargs):
        if int(kwargs['pk']) <= 0:
            self.kwargs['pk'] = kwargs['pk'] = str(request.user.id)
        if int(kwargs['pk']) == request.user.id:
            return super(getUserDetail, self).retrieve(request, *args, **kwargs)
        raise AuthenticationFailed('This is not you')

    def update(self, request, *args, **kwargs):
            # request.user = User.objects.get(pk=1)
        request.data['password'] = 'NOT_UPDATE' if request.data.get(
            'password', None) is None else request.data.get('password')
        print(request.user.password)
        print(request.data['password'])
        return super(getUserDetail, self).update(request, *args, **kwargs)


def bookListRedisKeys(view_instance, view_method, request, args, kwargs):
    total = Book.objects.all().count()
    page = request.query_params.get(
        'page') if request.query_params.get('page', None) else '1'
    return 'books_{}_p{}'.format(total, page)


class getAllBook(mixins.ListModelMixin, GenericViewSet):
    # queryset = Book.objects.all()
    serializer_class = bookSerializer
    pagination_class = bookPaging
    # permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        fav = favoriteBook.objects.filter(username=self.request.user.id).filter(
            isFavorite=True).values_list('bookname', flat=True)
        context = super(getAllBook, self).get_serializer_context()
        context.update({'favQuery': list(fav)})
        return context

    @cache_response(timeout=60 * 5, key_func=bookListRedisKeys)
    def list(self, request, *args, **kwargs):
        print(getAllBook.__mro__)
        order_field = request.GET.get(
            'order') if 'order' in request.GET else 'pk'

        self.queryset = Book.objects.order_by(order_field).select_related(
            'type').select_related('author')

        self.queryset = self.queryset.filter(name__contains=request.GET.get(
            'search')) if 'search' in request.GET else self.queryset

        return super(getAllBook, self).list(request, *args, **kwargs)


class favBook(mixins.CreateModelMixin, GenericViewSet):
    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = favoriteBook.objects.filter(username=self.request.user.id).filter(
                isFavorite=True).select_related('bookname').select_related('bookname__author').select_related(
                    'bookname__type')

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = bookFavGetSerializer
        elif self.request.method == 'POST':
            serializer_class = bookFavSerializer

        return serializer_class

    def list(self, request, *args, **kwargs):
        # self.request.user = User.objects.get(pk='1')

        serializer = self.get_serializer(self.get_queryset(), many=True)
        R = [{'username': self.request.user.username, 'data': serializer.data}]
        return Response(R, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # self.request.user = User.objects.get(pk='1')
        request.data if 'username' in request.data else request.data.update(
            {'username': self.request.user.id})

        return super(favBook, self).create(request, *args, **kwargs)
