import requests
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseBadRequest
from api.models import User


class ChatRoom(View):

    def get(self, request, *args, **kwargs):
        url = f'{settings.API_END_POINT}{reverse("api_v2:chat_check")}'

        headers = {
            'Authorization': 'JWT {}'.format(request.COOKIES.get('token', '')),
        }

        chat_check_resp = requests.get(url, headers=headers, verify=False)

        if chat_check_resp.status_code >= 400:
            return HttpResponseBadRequest(f'Error: {str(chat_check_resp.json())}')

        result = chat_check_resp.json()

        if not result['can_chat']:
            return HttpResponseBadRequest('Be friend first')

        context = {
            'chat_target': result['chat_target'],
            'group': f'{result["chat_from"]}_{result["chat_target"]}',
        }

        return render(request, 'chat.html', context=context)


class AdminChatRoom(View):

    def get(self, request, *args, **kwargs):
        chat_target = kwargs['target']

        if not chat_target:
            return HttpResponseBadRequest('Missing chat target')

        context = {
            'chat_target': chat_target,
            'group': f'{chat_target}_admin',
        }

        return render(request, 'chat.html', context=context)


def admin_chat_list(request, *args, **kwargs):
    users = User.objects.filter(is_active=True, is_staff=False)

    context = {
        'users': users,
    }

    return render(request, 'admin_chat_list.html', context=context)
