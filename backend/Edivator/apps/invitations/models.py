from django.db import models
from django.utils import timezone
import hashlib
import secrets

from apps.companies.models import Company
from apps.users.models import User


# Create your models here.

class Invitation(models.Model):
    """邀请码模型"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invitations', verbose_name='企业')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitings', verbose_name='被邀请')
    token = models.CharField(max_length=255, unique=True, verbose_name='邀请码')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    expires_at = models.DateTimeField(verbose_name='过期时间')
    is_accepted = models.BooleanField(default=False, verbose_name='是否已接受')

    class Meta:
        db_table = 'invitations'
        verbose_name = '邀请码'
        verbose_name_plural = '邀请码列表'

    def save(self, *args, **kwargs):
        # 假设我们在生成邀请码时直接设置一个过期时间
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)  # 假设邀请码有效期为7天
        super().save(*args, **kwargs)

    def generate_token(self):
        """生成秘钥"""
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((str(self.id) + salt).encode()).hexdigest()
        self.token = hashed[:16]  # 取前16位作为邀请码

    def __str__(self):
        return self.token
