from django.db import models

from apps.companies.models import Company
from apps.users.models import User
from common.db import BaseModel


# Create your models here.


class Team(BaseModel):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='teams', verbose_name='团队名')
    users = models.ManyToManyField(User, related_name='affiliated_teams', verbose_name='团队所属的企业', blank=True)
    description = models.TextField(verbose_name='团队描述', null=True, blank=True)
    avatar = models.ImageField(upload_to='team_avatars', null=True, blank=True, verbose_name='团队头像')
    cover = models.ImageField(upload_to='team_covers', null=True, blank=True, verbose_name='团队封面')

    class Meta:
        db_table = 'teams'
        verbose_name = '团队'
        verbose_name_plural = '团队列表'


class Message(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests', verbose_name='申请人')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_requests', verbose_name='申请的团队')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='状态')

    class Meta:
        db_table = 'messages'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField(verbose_name='通知内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'notifications'
