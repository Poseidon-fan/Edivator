from apps.chat.models import ChatMessage
from rest_framework import serializers

from apps.users.serializer import UserSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = '__all__'
