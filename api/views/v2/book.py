from api.models import Book
from api.serializers import BookSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.decorators import cache_response


def BookListRedisKeys(view_instance, view_method, request, args, kwargs):
    total = Book.objects.all().count()

    page = request.query_params.get(
        'page') if request.query_params.get('page', None) else '1'

    search = request.query_params.get(
        'search') if request.query_params.get('search', None) else 'none'

    order = request.query_params.get(
        'order') if request.query_params.get('order', None) else 'none'

    return 'books_{}_p{}_s{}_o{}'.format(total, page, search, order)


class BookPaging(PageNumberPagination):
    def get_paginated_response(self, data):
        current_page = int(self.request.query_params.get(self.page_query_param, 1))

        return Response({
            'total_page': self.page.paginator.num_pages,
            'current_page': current_page,
            'has_previous': self.page.has_previous(),
            'has_next': self.page.has_next(),
            'data': data
        })


class GetAllBook(mixins.ListModelMixin, GenericViewSet):
    serializer_class = BookSerializer
    pagination_class = BookPaging
    # permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('name', 'type__name')
    ordering = 'pk'

    def get_serializer_context(self):
        fav_books_q = self.request.user.favoritebook_set.favorited().values_list('book', flat=True)
        context = super(GetAllBook, self).get_serializer_context()
        context.update({'fav_books': [b for b in fav_books_q]})

        return context

    # @cache_response(timeout=60 * 5, key_func=BookListRedisKeys)
    def list(self, request, *args, **kwargs):
        # print(GetAllBook.__mro__)
        self.queryset = Book.objects. \
            select_related('type'). \
            select_related('author')

        return super(GetAllBook, self).list(request, *args, **kwargs)
