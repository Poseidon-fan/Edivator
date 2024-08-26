from rest_framework import serializers

from apps.companies.models import Company
from apps.teams.models import Team, Message, Notification


class TeamSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        source='company',
        queryset=Company.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Team
        fields = ['name', 'description', 'avatar', 'cover', 'company_id', 'id']
        extra_kwargs = {
            'company_id': {'required': True},
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
