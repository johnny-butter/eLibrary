from api.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.group = self.scope['url_route']['kwargs'].get('group', None)

        if isinstance(user, User):
            self.name = user.username
        else:
            self.close()

        if not self.group:
            self.close()

        # put channel in specific group
        async_to_sync(self.channel_layer.group_add)(
            self.group,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        # content -> json.loads(text_data) from receive method
        message = f'{content["message"]}'

        # send message to group channels
        self.group_send(message)

    def group_send(self, message, handler='chat_message'):
        # "type" is for designating function to handle message
        async_to_sync(self.channel_layer.group_send)(
            self.group,
            {
                'type': handler,
                'message': message,
                'username': self.name,
            }
        )

    # handler that designate from type
    def chat_message(self, event):
        content = {
            'message': event['message'],
            'username': event['username'],
        }

        # send message to websocket
        # send_json -> send(json.dumps(content))
        self.send_json(content)
