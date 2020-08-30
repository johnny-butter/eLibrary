import asyncio
import aiohttp
import requests
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect


async def get_response(url, params=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            return response.status, await response.json()


def book_list(request):
    q_string = {}
    for k in request.GET:
        q_string[k] = request.GET[k]

    headers = {
        'Authorization': f"JWT {request.COOKIES.get('token', '')}",
    }

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    tasks = (
        asyncio.ensure_future(get_response(f'{settings.API_END_POINT}{reverse("api_v2:getAllBookCbv")}', params=q_string, headers=headers)),
        asyncio.ensure_future(get_response(f'{settings.API_END_POINT}{reverse("api_v2:book_top3")}', headers=headers)),
    )

    # asyncio.wait(): accept list;
    # asyncio.gather(): accept many tasks;

    # results = loop.run_until_complete(asyncio.wait(tasks))
    results = loop.run_until_complete(asyncio.gather(*tasks))

    (books_status, books_resp), (book_top3_status, book_top3_resp) = results

    if 200 <= books_status < 400:
        context = {
            'books': books_resp['data'],
            'pages': books_resp['total_page'],
            'current_page': books_resp['current_page'],
            'has_previous': books_resp['has_previous'],
            'has_next': books_resp['has_next'],
            'book_top3': book_top3_resp,
        }

        return render(request, 'book_list.html', context=context)
    else:
        return HttpResponseBadRequest(f'Error:{books_resp}')


def fav_book_list(request):
    fav_books = requests.get(
        f'{settings.API_END_POINT}{reverse("api_v2:favBookCbv")}',
        headers={'Authorization': f"JWT {request.COOKIES.get('token', '')}"},
        verify=False
    )

    if 200 <= fav_books.status_code < 400:
        return render(request, 'fav_book_list.html', context={'favbooks': fav_books.json()})
    else:
        return HttpResponseBadRequest(f'Error: {fav_books.json()}')


def user_info_page(request):
    if request.method == 'GET':
        url = f'{settings.API_END_POINT}{reverse("api_v2:user_cbv")}'

        headers = {
            'Authorization': f"JWT {request.COOKIES.get('token', '')}",
        }

        userinfo = requests.get(url, headers=headers, verify=False)

        if 200 <= userinfo.status_code < 400:
            return render(request, 'user_info.html', context={'user': userinfo.json()})
        else:
            return HttpResponseBadRequest(f'Error: {str(userinfo.json())}')
