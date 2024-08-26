from rest_framework import serializers

from apps.companies.models import Company
from apps.invitations.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(
        source='company',
        queryset=Company.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Invitation
        fields = ['company_id', 'user_id', 'token']
        extra_kwargs = {
            'company_id': {'required': True},
        }

    def create(self, validated_data):
        company_id = validated_data.pop('company').id

        # 创建Invitation实例，但不设置token和expires_at（这些将在save方法中处理）
        invitation = Invitation(**validated_data)

        # 调用generate_token方法来设置token
        invitation.generate_token()

        # 查找相应的Company并设置到Invitation上
        company = Company.objects.get(pk=company_id)
        invitation.company = company

        # 保存Invitation实例，这会触发save方法中的逻辑来设置expires_at
        invitation.save()

        return invitation
