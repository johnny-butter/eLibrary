import requests
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest


def login_page(request):
    if request.method == 'GET':
        return render(request, 'login_page.html')
