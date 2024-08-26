from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.companies.models import Company
from apps.users.permissions import UserPermission

from apps.invitations.models import Invitation
from apps.invitations.serializers import InvitationSerializer


# Create your views here.


class InvitationViewSet(ModelViewSet):
    """验证码模型"""
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated, UserPermission]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        company_id = request.data.get('company_id')
        user_id = request.data.get('user_id')
        if not company_id:
            return Response({'error': '提交数据缺失'}, status=status.HTTP_400_BAD_REQUEST)

        # 校验 company_id是否匹配
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({'error': '公司不存在'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={
            'company_id': company_id,
            'user_id': user_id,
            'token': '1'
        })

        # 确保数据有效
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
