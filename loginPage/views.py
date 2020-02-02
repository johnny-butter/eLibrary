import requests
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest


def loginPage(request):
    if request.method == 'GET':
        return render(request, 'loginPage.html')
