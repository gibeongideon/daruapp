# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import daru_wheel.routing

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter(
#     {
#         # Django's ASGI application to handle traditional HTTP requests
#         "http": django_asgi_app,  # http is added by default in production
#         "websocket": AuthMiddlewareStack(
#             URLRouter(daru_wheel.routing.websocket_urlpatterns)
#         ),
#     }
# )
