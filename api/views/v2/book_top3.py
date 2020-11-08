from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework_extensions.cache.decorators import cache_response


class GetBookTop3(ViewSet):

    @cache_response(timeout=60 * 60 * 1, key_func=BookTop3.top3_cache_key)
    def list(self, request, *args, **kwargs):
        current_time = (datetime.now() + timedelta(hours=-1)).strftime('%Y%m%d%H')

        query_result = BookTop3.objects. \
            filter(count_time=current_time). \
            order_by('-book_count'). \
            values_list('book__name', flat=True).distinct()

        resp = [book for book in query_result] if query_result else []

        return Response(resp)
