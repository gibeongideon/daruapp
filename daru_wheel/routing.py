from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/daru_wheel/', consumers.SpinConsumer.as_asgi()),
    re_path(r'ws/ispin_wheel/', consumers.QspinConsumer.as_asgi()),

]
