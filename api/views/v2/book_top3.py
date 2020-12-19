from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_extensions.cache.decorators import cache_response

from api.models import BookTop3, Book


class GetBookTop3(ViewSet):

    @cache_response(timeout=60 * 60 * 1, key_func=BookTop3.top3_cache_key)
    def list(self, request, *args, **kwargs):
        current_time = (datetime.now() + timedelta(hours=-1)).strftime('%Y%m%d%H')

        query_result = BookTop3.objects. \
            filter(count_time=current_time). \
            order_by('-book_count'). \
            values_list('book__name', flat=True).distinct()

        if not query_result:
            query_result = Book.objects.all().order_by('?').values_list('name', flat=True)[:5]

        resp = {'books_names': [book_name for book_name in query_result]}

        return Response(resp)
