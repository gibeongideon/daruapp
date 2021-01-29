from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/spinchannel/', consumers.SpinConsumer.as_asgi()),
    # re_path(r'ws/timerchannel/', consumers.TimerConsumer.as_asgi()),
    
]