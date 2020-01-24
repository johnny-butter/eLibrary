from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import User, Book, favoriteBook
from api.serializers import userSerializer, bookSerializer, bookFavSerializer, bookFavGetSerializer
from json_reader import JsonReader
from rest_framework.exceptions import NotFound


@api_view(['GET', 'POST'])
def getUserList(request):
    if request.method == 'GET':

        serializer = userSerializer(User.objects.all(), many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        data = JsonReader.read_body(request)
        serializer = userSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def getUserDetail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': "User " + pk + " does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = userSerializer(user)

        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JsonReader.read_body(request)
        serializer = userSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def getAllBook(request):
    if request.method == 'GET':
        orderItem = request.GET.get(
            'order') if 'order' in request.GET else 'pk'

        fav = favoriteBook.objects.filter(user=request.user.id).filter(
            isFavorite=True).values_list('book', flat=True)

        def paginF(queryset, itemPerPage=5):
            totalPage, hasPrevious, hasNext = 1, False, False
            nowPage = 1 if request.GET.get(
                'page') is None else request.GET.get('page')

            if 'page' in request.GET:
                pagin = Paginator(queryset, itemPerPage)

                totalPage = len(list(pagin.page_range))
                nowPage = 1 if int(nowPage) < 1 else int(nowPage)
                queryset = pagin.page(nowPage)
                hasPrevious = queryset.has_previous()
                hasNext = queryset.has_next()

            return queryset, {'total_page': totalPage,
                              'current_page': nowPage,
                              'has_previous': hasPrevious,
                              'has_next': hasNext}

        if 'search' in request.GET:
            books = Book.objects.filter(name__contains=request.GET.get('search')).order_by(
                orderItem).select_related('type').select_related('author')
        else:
            books = Book.objects.order_by(orderItem).select_related(
                'type').select_related('author')

        try:
            books, pageInfo = paginF(books)
            serializer = bookSerializer(books, many=True, context={
                'favQuery': list(fav)})
        except:
            raise NotFound(detail='Invalid page')

        pageInfo.update({'data': serializer.data})

        return Response(pageInfo)


@api_view(['GET', 'POST'])
def favBook(request):
    if request.method == 'GET':
        favbooklist = favoriteBook.objects.filter(username=request.user.id).filter(isFavorite=True).select_related(
            'book').select_related('book__author').select_related('book__type')

        serializer = bookFavGetSerializer(favbooklist, many=True)

        R = [{'username': request.user.username, 'data': serializer.data}]

        return Response(R, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = JsonReader.read_body(request).copy()
        if 'username' not in data:
            data['username'] = request.user.id
        serializer = bookFavSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
