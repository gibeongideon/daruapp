
# release: python manage.py migrate
# web: daphne daruapp.asgi:application --port $PORT --bind 0.0.0.0 -v2
# worker: python manage.py runworker channels --settings=daruapp.settings -v2

# daphne -p 8001 daruapp.asgi:application

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import daru_wheel.routing
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,    #ttp is added by default in production
    'websocket': AuthMiddlewareStack(
        URLRouter(
            daru_wheel.routing.websocket_urlpatterns
        )
    ),
})

