import requests
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest


def pay_page(request):
    if request.method == 'GET':
        headers = {'Authorization': 'JWT ' + request.COOKIES.get('token', '')}

        result = requests.get(f'{settings.API_END_POINT}{reverse("api_v2:shopCar")}', headers=headers)

        books = result.json().get('results', None)
        amount = 0
        for book in books:
            quantity = book.get('quantity', 0)
            price = book.get('book_price', 0)
            amount += int(price) * int(quantity)
        if result.ok:
            return render(request, 'payment.html', context={'books': books,
                                                            'amount': amount, })
        else:
            return HttpResponseBadRequest('Error: {}'.format(result.json()))
