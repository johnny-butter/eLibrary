import braintree
import requests
import json
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

# Create your views here.


def payPage(request):
    if request.method == 'GET':
        headers = {'Authorization': 'JWT ' + request.COOKIES.get('token', '')}

        result = requests.get(request.build_absolute_uri(
            reverse('api_v2:shopCar')), headers=headers)

        books = json.loads(result.content).get('results', None)
        amount = 0
        for book in books:
            quantity = book.get('quantity', 0)
            price = book.get('book_price', 0)
            amount += int(price) * int(quantity)
        if result.ok:
            return render(request, 'payment.html', context={'books': books,
                                                            'amount': amount, })
        else:
            return HttpResponseBadRequest('Error:' + str(json.loads(result.content)))
