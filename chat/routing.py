from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'/send_message/', consumers.ChatConsumer.as_asgi()),
]
