from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os
import django
import xerox_machine.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xerox_machine.settings')

print("\nIn asgi.py baby\n")

websocket=URLRouter(xerox_machine.routing.websocket_urlpatterns)
print(websocket)

urls = xerox_machine.routing.websocket_urlpatterns
application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            xerox_machine.routing.websocket_urlpatterns
        )
    ),
    "channel": xerox_machine.routing.channel_routing,
})