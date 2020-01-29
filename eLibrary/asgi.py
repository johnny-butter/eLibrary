from channels.routing import ProtocolTypeRouter, URLRouter
from shared.channel_jwt_validate import JWTAuthMiddlewareStack
from chat import routing


application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
})
