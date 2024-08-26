from django.db import models
from common.db import BaseModel
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser, BaseModel):
    """用户模型"""
    mobile = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='user_avatars', null=True, blank=True, verbose_name='用户头像')
    point = models.IntegerField(default=100, null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'

