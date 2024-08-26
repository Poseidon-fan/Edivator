from django.db import models

from apps.teams.models import Team
from apps.users.models import User


# Create your models here.

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages', db_index=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='chat_messages', db_index=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='messages', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        ordering = ('created_at',)

