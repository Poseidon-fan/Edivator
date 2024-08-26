from django.db import models

from apps.users.models import User
from common.db import BaseModel


# Create your models here.


class Dialog(BaseModel):
    TYPE_CHOICES = (
        ('bot', 'Bot'),
        ('user', 'User'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialogs')
    text = models.TextField()
    sender = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        db_table = 'dialog'
        verbose_name = '对话记录'
        verbose_name_plural = '对话记录列表'

