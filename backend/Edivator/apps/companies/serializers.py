from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """企业序列化容器"""
    class Meta:
        model = Company
        fields = '__all__'



