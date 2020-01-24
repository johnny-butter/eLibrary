from api.models import Book
from api.serializers import bookSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.decorators import cache_response


def bookListRedisKeys(view_instance, view_method, request, args, kwargs):
    total = Book.objects.all().count()

    page = request.query_params.get(
        'page') if request.query_params.get('page', None) else '1'

    search = request.query_params.get(
        'search') if request.query_params.get('search', None) else 'none'

    order = request.query_params.get(
        'order') if request.query_params.get('order', None) else 'none'

    return 'books_{}_p{}_s{}_o{}'.format(total, page, search, order)


class bookPaging(PageNumberPagination):
    def get_paginated_response(self, data):
        nowPage = int(self.request.query_params.get(self.page_query_param, 1))
        return Response({'total_page': self.page.paginator.num_pages,
                         'current_page': nowPage,
                         'has_previous': self.page.has_previous(),
                         'has_next': self.page.has_next(),
                         'data': data})


class getAllBook(mixins.ListModelMixin, GenericViewSet):
    # queryset = Book.objects.all()
    serializer_class = bookSerializer
    pagination_class = bookPaging
    # permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('name', 'type__name')
    # ordering_fields = ('price_discount',)
    ordering = 'pk'

    def get_serializer_context(self):
        fav = self.request.user.favoritebook_set.favorited().values_list('book', flat=True)
        context = super(getAllBook, self).get_serializer_context()
        context.update({'favQuery': [favBook for favBook in fav]})

        return context

    # @cache_response(timeout=60 * 5, key_func=bookListRedisKeys)
    def list(self, request, *args, **kwargs):
        # print(getAllBook.__mro__)
        self.queryset = Book.objects.select_related(
            'type').select_related('author')
        # order_field = request.GET.get(
        #     'order') if 'order' in request.GET else 'pk'

        return super(getAllBook, self).list(request, *args, **kwargs)
