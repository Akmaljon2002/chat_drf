from django.urls import path
from chat.views import send_message, get_messages

urlpatterns = [
    path('send_message/', send_message),
    path('get_messages/', get_messages),
]
