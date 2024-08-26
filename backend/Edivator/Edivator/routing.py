from channels.routing import URLRouter
from django.urls import re_path, path

from apps.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:team_id>/', ChatConsumer.as_asgi()),
]