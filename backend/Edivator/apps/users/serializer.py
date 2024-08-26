from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户模型的序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'avatar', 'point']
