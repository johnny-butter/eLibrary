import requests
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseBadRequest


def pay_page(request):
    if request.method == 'GET':
        headers = {'Authorization': f"JWT {request.COOKIES.get('token', '')}"}

        result = requests.get(f'{settings.API_END_POINT}{reverse("api_v2:shop_car")}', headers=headers)

        if not result.ok:
            return HttpResponseBadRequest(f'Error: {result.json()}')

        books = result.json().get('results', [])
        amount = 0
        for book in books:
            quantity = book.get('quantity', 0)
            price = book.get('book_price', 0)
            amount += int(price) * int(quantity)

        context = {'books': books, 'amount': amount}

        return render(request, 'payment.html', context=context)
