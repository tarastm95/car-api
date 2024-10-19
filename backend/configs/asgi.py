import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from core.middlewares.auth_socket_middleware import AuthSocketMiddleware

from configs.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': AuthSocketMiddleware(URLRouter(websocket_urlpatterns))
})
