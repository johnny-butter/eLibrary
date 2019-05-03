from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Book, favoriteBook
from .serializers import userSerializer, bookSerializer, bookFavSerializer, bookFavGetSerializer
from jsonreader import JsonReader
from .voter import userVoter
from rest_framework.exceptions import NotFound
import urllib
import requests
import json

# Create your views here.
@api_view(['GET', 'POST'])
def getUserList(request):
    """
    get:
    List all users.
    post:
    Create new user.
    """
    print(request.user)
    print(str(request.auth))

    if request.method == 'GET':
        if not userVoter(request).is_logged_in():
            return Response({'error': "No auth"}, status=status.HTTP_400_BAD_REQUEST)

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
    """
    get:
    Detail one user.
    put:
    Update one user.
    delete:
    Delete one user.
    """
    if not userVoter(request).is_logged_in():
        return Response({'error': "No auth"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=pk)
        print(user)
    except User.DoesNotExist:
        return Response({'error': "User " + pk + " does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if not userVoter(request).user_can_manage_me(user):
        return Response({'error': "No permission"}, status=status.HTTP_400_BAD_REQUEST)

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


# @api_view(['POST'])
# def api_login(request):
#     """
#     post:
#     This view is called through API POST with a json body
#     """
#     data = JsonReader.read_body(request)

#     response_login = requests.post(
#         request.build_absolute_uri(reverse('token_obtain_pair')),
#         data=data
#     )
#     response_login_dict = json.loads(response_login.content)
#     return Response(response_login_dict, response_login.status_code)


@api_view(['GET'])
def getAllBook(request):
    if request.method == 'GET':
        # if not userVoter(request).is_logged_in():
        #     return Response({'error': "No auth"}, status=status.HTTP_400_BAD_REQUEST)
        orderItem = request.GET.get(
            'order') if 'order' in request.GET else 'pk'

        fav = favoriteBook.objects.filter(username=request.user.id).filter(
            isFavorite=True).values_list('bookname', flat=True)

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
            # Q = urllib.parse.unquote(request.GET.get('search'))
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
            # return Response({'detail': 'Invalid page'}, status=status.HTTP_404_NOT_FOUND)

        pageInfo.update({'data': serializer.data})
        return Response(pageInfo)


@api_view(['GET', 'POST'])
def favBook(request):
    if request.method == 'GET':
        # print(request.user.id)
        favbooklist = favoriteBook.objects.filter(username=request.user.id).filter(isFavorite=True).select_related(
            'bookname').select_related('bookname__author').select_related('bookname__type')

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
