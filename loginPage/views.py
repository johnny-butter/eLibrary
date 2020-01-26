import requests
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest


def loginPage(request):
    if request.method == 'GET':
        return render(request, 'loginPage.html')


def registerPage(request):
    if request.method == 'GET':
        return render(request, 'registerPage.html')

    if request.method == 'POST':

        data = request.POST
        register_response = requests.post(request.build_absolute_uri(reverse('getUserListCbv')),
                                          json={'username': data.get('username'),
                                                'password': data.get('password'),
                                                'email': data.get('email')})

    if register_response.status_code >= 200 and register_response.status_code < 400:

        response = HttpResponseRedirect(reverse('loginPage'))

        return response

    else:
        return HttpResponseBadRequest(register_response.content)
