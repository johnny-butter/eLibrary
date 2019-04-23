from django.shortcuts import render
from jsonreader import JsonReader
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
import requests
import json
# Create your views here.


def loginPage(request):
    if request.method == 'GET':
        return render(request, 'loginPage.html')

    # if request.method == 'POST':
    #     '''
    #     request.POST return dict-like data
    #     use in content type == application/x-www-form-urlencoded
    #     request.body use in content type == application/json
    #     '''

    #     data = request.POST
    #     response_login = requests.post(
    #         request.build_absolute_uri(reverse('token_obtain_pair')),
    #         json={'username': data.get('username'),
    #               'password': data.get('password')}
    #     )
    #     if response_login.status_code >= 200 and response_login.status_code < 400:
    #         response_login_dict = json.loads(response_login.content)

    #         response = HttpResponseRedirect(reverse('booklist') + '?page=1')
    #         response.set_cookie(
    #             'token', response_login_dict['access'], 3600)
    #         response.set_cookie(
    #             'token_r', response_login_dict['refresh'], 3600)

    #         return response
    #     else:
    #         return HttpResponseBadRequest(response_login.content)


def registerPage(request):
    if request.method == 'GET':
        return render(request, 'registerPage.html')

    if request.method == 'POST':

        data = request.POST
        register_response = requests.post(request.build_absolute_uri(reverse('getUserList')),
                                          json={'username': data.get('username'),
                                                'password': data.get('password'),
                                                'email': data.get('email')})

    if register_response.status_code >= 200 and register_response.status_code < 400:
        # register_response_dict = json.loads(register_response.content)

        response = HttpResponseRedirect(reverse('loginPage'))

        return response

    else:
        return HttpResponseBadRequest(register_response.content)
