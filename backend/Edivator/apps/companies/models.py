from django.db import models
from django.utils import timezone

from apps.users.models import User
from common.db import BaseModel


# Create your models here.

class Company(BaseModel):
    """企业表"""
    name = models.CharField(max_length=255, unique=True, verbose_name='企业名称')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_companies', verbose_name='企业创建者')
    description = models.TextField(verbose_name='企业描述')
    users = models.ManyToManyField(User, related_name='affiliated_companies', verbose_name='企业人员', blank=True)
    administrators = models.ManyToManyField(User, related_name='admin_teams', verbose_name='团队管理员', blank=True)
    class Meta:
        db_table = 'companies'
        verbose_name = '企业'
        verbose_name_plural = '公司列表'



