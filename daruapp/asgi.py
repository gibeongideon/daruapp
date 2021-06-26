"""
ASGI config for daruapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daruapp.settings")
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import daru_wheel.routing

asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    daru_wheel.routing.websocket_urlpatterns
                )
            )
        ),
    }
)


# application = ProtocolTypeRouter({
#     "http": asgi_app,
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             daru_wheel.routing.websocket_urlpatterns
#         )
#     )
# })