"""
ASGI config for daruapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os
# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import daru_wheel.routing
from channels.security.websocket import AllowedHostsOriginValidator
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daruapp.settings")
django.setup()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AllowedHostsOriginValidator(
    #   AuthMiddlewareStack(
        URLRouter(
            daru_wheel.routing.websocket_urlpatterns
            )
        # ),
    ),

})
