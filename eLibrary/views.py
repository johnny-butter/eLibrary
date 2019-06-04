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

    url = request.build_absolute_uri(reverse('getAllBookCbv')) + qString

    books = requests.get(
        url,
        headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')},
        verify=False
    )

    fav = requests.get(
        request.build_absolute_uri(reverse('favBookCbv')),
        headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')},
        verify=False
    )

    if books.ok and fav.ok:
        bResponseData = json.loads(books.content)
        fResponseData = json.loads(fav.content)
        print(fResponseData)
        favBooks = [info['bookname'] for info in fResponseData[0]['data']]
        return render(request, 'bookList.html', context={'books': bResponseData['data'],
                                                         'pages': bResponseData['total_page'],
                                                         'current_page': bResponseData['current_page'],
                                                         'has_previous': bResponseData['has_previous'],
                                                         'has_next': bResponseData['has_next'],
                                                         'fav': favBooks})
    else:
        return HttpResponseBadRequest('Error:' + str(json.loads(books.content)))


def favBookList(request):
    favbooks = requests.get(request.build_absolute_uri(reverse('favBookCbv')),
                            headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')}, verify=False)

    if favbooks.status_code >= 200 and favbooks.status_code < 400:
        return render(request, 'favBookList.html', context={'favbooks': json.loads(favbooks.content)[0]})
    else:
        print(favbooks.status_code)
        return HttpResponseBadRequest('Error:' + str(json.loads(favbooks.content)))


def userInfoPage(request):
    if request.method == 'GET':
        url = request.build_absolute_uri(
            reverse('getUserDetailCbv', args=(0,)))
        print(url)
        userinfo = requests.get(
            url, headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')}, verify=False)
        if userinfo.status_code >= 200 and userinfo.status_code < 400:
            return render(request, 'userInfo.html', context={'user': json.loads(userinfo.content)})
        else:
            return HttpResponseBadRequest('Error:' + str(json.loads(userinfo.content)))
