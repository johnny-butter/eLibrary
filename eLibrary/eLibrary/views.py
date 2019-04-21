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

    if qString:
        qString = '?' + qString[:-1]

    url = request.build_absolute_uri(reverse('getAllBook')) + qString

    # if request.GET.get('search') is None:
    #     url = request.build_absolute_uri(reverse('getAllBook'))
    # else:
    #     url = request.build_absolute_uri(
    #         reverse('getAllBook')) + '?search=' + request.GET.get('search')

    books = requests.get(
        url,
        headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')}
    )
    if books.status_code >= 200 and books.status_code < 400:
        print(books.content)
        return render(request, 'bookList.html', context={'books': json.loads(books.content)})
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
