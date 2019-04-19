from django.shortcuts import render
from jsonreader import JsonReader
from django.urls import reverse
from globalvar import authHeader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
import requests
import json
# Create your views here.


def loginPage(request):
    if request.method == 'GET':
        return render(request, 'loginPage.html')

    if request.method == 'POST':
        # request.POST return dict-like data
        # use in content type == application/x-www-form-urlencoded
        # request.body use in content type == application/json
        data = request.POST
        print(data)
        response_login = requests.post(
            request.build_absolute_uri(reverse('token_obtain_pair')),
            json={'username': data.get('username'),
                  'password': data.get('password')}
        )
        if response_login.status_code >= 200 and response_login.status_code < 400:
            response_login_dict = json.loads(response_login.content)
            authHeader.accessToken = response_login_dict['access']
            authHeader.refreshToken = response_login_dict['refresh']
            print(authHeader.accessToken)
            return HttpResponseRedirect(reverse('booklist'))
        else:
            return HttpResponseBadRequest(response_login.content)
            # return render(request, 'loginPage.html')
