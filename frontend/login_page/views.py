from django.shortcuts import render
from django.http import HttpResponseBadRequest


def login_page(request):
    if not request.method == 'GET':
        return HttpResponseBadRequest('Not supported method')

    return render(request, 'login_page.html')
