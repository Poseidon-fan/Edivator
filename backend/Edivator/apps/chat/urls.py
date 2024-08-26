from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps import ai
from apps.chat.views import ChatMessageViewSet


urlpatterns = [
    path('query/', ChatMessageViewSet.as_view({'get': 'query'})),
]
