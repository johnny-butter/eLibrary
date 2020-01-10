from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
import asyncio
import aiohttp
import functools
import requests
import json
import time


async def get_response(url, params=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            return response.status, await response.text()


def bookList(request):
    qString = {}
    for qKey in ['search', 'search', 'order']:
        if request.GET.get(qKey, None):
            qString[qKey] = request.GET.get(qKey)

    headers = {'Authorization': 'JWT ' + request.COOKIES.get('token', '')}

    print('S:' + str(time.time()))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    tasks = (
        asyncio.ensure_future(asyncio.ensure_future(get_response(request.build_absolute_uri(
            reverse('api_v2:getAllBookCbv')), params=qString, headers=headers))),
        asyncio.ensure_future(get_response(request.build_absolute_uri(
            reverse('api_v2:favBookCbv')), params=qString, headers=headers))
    )

    # asyncio.wait(): accept list;
    # asyncio.gather(): accept many tasks;

    # loop.run_until_complete(asyncio.wait(tasks))
    results = loop.run_until_complete(asyncio.gather(*tasks))

    books = results[0]
    fav = results[1]
    print('F:' + str(time.time()))

    bResponseData = json.loads(books[1])
    fResponseData = json.loads(fav[1])

    if (books[0] >= 200 and books[0] < 400) and (fav[0] >= 200 and fav[0] < 400):
        favBooks = [info['bookname'] for info in fResponseData[0]['data']]
        return render(request, 'bookList.html', context={'books': bResponseData['data'],
                                                         'pages': bResponseData['total_page'],
                                                         'current_page': bResponseData['current_page'],
                                                         'has_previous': bResponseData['has_previous'],
                                                         'has_next': bResponseData['has_next'],
                                                         'fav': favBooks})
    else:
        return HttpResponseBadRequest('Error:{}'.format(bResponseData))


def favBookList(request):
    favbooks = requests.get(request.build_absolute_uri(reverse('api_v2:favBookCbv')),
                            headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')}, verify=False)

    if favbooks.status_code >= 200 and favbooks.status_code < 400:
        return render(request, 'favBookList.html', context={'favbooks': json.loads(favbooks.content)[0]})
    else:
        print(favbooks.status_code)
        return HttpResponseBadRequest('Error:' + str(json.loads(favbooks.content)))


def userInfoPage(request):
    if request.method == 'GET':
        url = request.build_absolute_uri(
            reverse('api_v2:getUserDetailCbv', args=(0,)))
        print(url)
        userinfo = requests.get(
            url, headers={'Authorization': 'JWT ' + request.COOKIES.get('token', '')}, verify=False)
        if userinfo.status_code >= 200 and userinfo.status_code < 400:
            return render(request, 'userInfo.html', context={'user': json.loads(userinfo.content)})
        else:
            return HttpResponseBadRequest('Error:' + str(json.loads(userinfo.content)))
