import base64
import json
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from .models import ChatMessage
from ..teams.models import Team

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope['url_route']['kwargs'])
        self.team_id = self.scope['url_route']['kwargs']['team_id']
        self.user_id = self.scope['query_string'].decode().split('=')[1]

        self.group_name = f'chat_{self.team_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        # 调试输出
        print(f"Received message from user_id: {self.user_id} in group_id: {self.team_id}")

        try:
            sender = User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            print(f"User with id {self.user_id} does not exist")
            return

        team = Team.objects.get(id=self.team_id)

        image_data = data.get('image')
        image = None

        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name=f'{sender.username}_{time.time()}.{ext}')

        message = ChatMessage.objects.create(
            sender=sender,
            team=team,
            text=data.get('text'),
            image=image
        )

        response = {
            'id': message.id,
            'sender': {
                'username': message.sender.username,
                'id': message.sender.id
            },
            'team': message.team.id,
            'text': message.text,
            'image': message.image.url if message.image else None,
            'created_at': message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(response)
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=message)
