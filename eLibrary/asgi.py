from channels.routing import ProtocolTypeRouter, URLRouter
from shared.validations import JWTAuthMiddlewareStack
from chat import routing


application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
})
