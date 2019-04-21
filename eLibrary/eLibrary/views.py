from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
# from jsonreader import JsonReader
import requests
import json


def bookList(request):
    qString = ''
    if 'search' in request.GET:
        qString += 'search=' + request.GET.get('search') + '&'
    if 'page' in request.GET:
        qString += 'page=' + request.GET.get('page') + '&'
    if 'order' in request.GET:
        qString += 'order=' + request.GET.get('order') + '&'

    if qString:
        qString = '?' + qString[:-1]

    url = request.build_absolute_uri(reverse('getAllBook')) + qString

    books = requests.get(
        url,
        headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')}
    )
    if books.status_code >= 200 and books.status_code < 400:
        responseData = json.loads(books.content)
        return render(request, 'bookList.html', context={'books': responseData['data'],
                                                         'pages': responseData['total_page'],
                                                         'current_page': responseData['current_page'],
                                                         'has_previous': responseData['has_previous'],
                                                         'has_next': responseData['has_next']})
    else:
        return HttpResponseBadRequest('No auth >___<')


def favBookList(request):
    favbooks = requests.get(request.build_absolute_uri(reverse('favBook')),
                            headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')})

    if favbooks.status_code >= 200 and favbooks.status_code < 400:
        return render(request, 'favBookList.html', context={'favbooks': json.loads(favbooks.content)[0]})
    else:
        print(favbooks.status_code)
        return HttpResponseBadRequest('No auth >___<')
