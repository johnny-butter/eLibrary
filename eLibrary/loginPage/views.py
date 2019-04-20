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

    if request.method == 'POST':
        '''
        request.POST return dict-like data
        use in content type == application/x-www-form-urlencoded
        request.body use in content type == application/json
        '''

        data = request.POST
        print(data)
        response_login = requests.post(
            request.build_absolute_uri(reverse('token_obtain_pair')),
            json={'username': data.get('username'),
                  'password': data.get('password')}
        )
        if response_login.status_code >= 200 and response_login.status_code < 400:
            response_login_dict = json.loads(response_login.content)

            response = HttpResponseRedirect(reverse('booklist'))
            response.set_cookie(
                'token', response_login_dict['access'], 3600)
            response.set_cookie(
                'token_r', response_login_dict['refresh'], 3600)

            return response
        else:
            return HttpResponseBadRequest(response_login.content)
            # return render(request, 'loginPage.html')
