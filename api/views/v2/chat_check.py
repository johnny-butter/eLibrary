from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated


class ChatCheck(GenericViewSet):

    permission_classes = [IsAuthenticated]

    def check(self, request, *args, **kwargs):
        chat_target = request.query_params.get('target', 'admin')

        resp = {
            'chat_from': request.user.username,
            'chat_target': chat_target,
            'can_chat': True,
        }

        return Response(resp, status=status.HTTP_200_OK)
