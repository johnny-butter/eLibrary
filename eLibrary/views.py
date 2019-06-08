from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
# from jsonreader import JsonReader
import asyncio
import functools
import requests
import json
import time


async def get_response(url, eventLoop, headers=None, method='get'):
    req = getattr(requests, method)
    # res = req(url, headers=headers, verify=False)
    res = await eventLoop.run_in_executor(None, functools.partial(
        req, url, headers=headers, verify=False))
    return res


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

    headers = {'Authorization': 'JWT ' + request.COOKIES.get('token', '')}
    print('S:' + str(time.time()))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    tasks = (
        asyncio.ensure_future(get_response(request.build_absolute_uri(
            reverse('getAllBookCbv')), loop, headers=headers)),
        asyncio.ensure_future(get_response(request.build_absolute_uri(
            reverse('favBookCbv')), loop, headers=headers))
    )

    # loop.run_until_complete(asyncio.wait(tasks))
    results = loop.run_until_complete(asyncio.gather(*tasks))
    # print(results)
    books = results[0]
    fav = results[1]

    # url = request.build_absolute_uri(reverse('getAllBookCbv')) + qString

    # books = requests.get(
    #     url,
    #     headers=headers,
    #     verify=False
    # )

    # fav = requests.get(
    #     request.build_absolute_uri(reverse('favBookCbv')),
    #     headers=headers,
    #     verify=False
    # )

    if books.ok and fav.ok:
        print('F:' + str(time.time()))
        bResponseData = json.loads(books.content)
        fResponseData = json.loads(fav.content)
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
