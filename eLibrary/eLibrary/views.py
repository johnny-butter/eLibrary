from django.shortcuts import render
# from jsonreader import JsonReader
from django.urls import reverse
from globalvar import authHeader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
import requests
import json


def bookList(request):
    books = requests.get(
        request.build_absolute_uri(reverse('getAllBook')),
        headers={'Authorization': 'JWT ' + authHeader.accessToken}
    )
    if books.status_code >= 200 and books.status_code < 400:
        print(books.content)
        return render(request, 'bookList.html', context={'books': json.loads(books.content),
                                                         'pass': authHeader.accessToken})
    else:
        return HttpResponseBadRequest('No auth >___<')


def favBookList(request):
    favbooks = requests.get(request.build_absolute_uri(reverse('favBook')),
                            headers={'Authorization': 'JWT ' + authHeader.accessToken})

    if favbooks.status_code >= 200 and favbooks.status_code < 400:
        return render(request, 'favBookList.html', context={'favbooks': json.loads(favbooks.content)[0]})
    else:
        print(favbooks.status_code)
        return HttpResponseBadRequest('No auth >___<')
