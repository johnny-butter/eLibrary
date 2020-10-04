import requests
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseBadRequest


def pay_page(request):
    if request.method == 'GET':
        headers = {'Authorization': f"JWT {request.COOKIES.get('token', '')}"}

        ret = requests.get(f'{settings.API_END_POINT}{reverse("api_v2:pay_order")}', headers=headers)

        if ret.ok:
            books = ret.json().get('data', {}).get('item_list', [])
            total_amount = sum([float(b.get('quantity', '0')) * float(b.get('price', '0')) for b in books])
        else:
            ret = requests.get(f'{settings.API_END_POINT}{reverse("api_v2:shop_car")}', headers=headers)

            if not ret.ok:
                HttpResponseBadRequest(f'Error: {ret.json()}')

            books = ret.json().get('results', [])
            total_amount = sum([float(b.get('quantity', '0')) * float(b.get('book_price', '0')) for b in books])

        context = {'books': books, 'amount': total_amount}

        return render(request, 'payment.html', context=context)
