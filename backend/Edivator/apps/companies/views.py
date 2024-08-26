from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from apps.teams.serializer import TeamSerializer
from apps.users.models import User
from apps.users.permissions import UserPermission
from apps.users.serializer import UserSerializer
from common.utils import check_is_all


# Create your views here.


class CompaniesViewSet(ModelViewSet):
    """企业视图集"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        description = request.data['description']
        admin = request.user.id
        if not check_is_all([name, description, admin]):
            return Response({'error': '参数不全'}, status=403)

        serializer = self.get_serializer(data={
            'name': name,
            'description': description,
            'admin': admin
        })

        # 确保数据有效
        serializer.is_valid(raise_exception=True)

        # 保存企业
        company = serializer.save()

        # 把当前的用户加到企业user里
        company.users.add(request.user)
        company.administrators.add(request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def appoint_administrator(self, request, *args, **kwargs):
        """指定企业管理员"""
        company_id = request.data.get('company_id')
        target_user_id = request.data.get('target_user_id')
        if not check_is_all([company_id, target_user_id]):
            return Response({'error': '参数不全'}, status=403)

        try:
            company = Company.objects.get(id=company_id)
            user = User.objects.get(id=target_user_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if company.admin.id != request.user.id:
            return Response({'error': '无权操作'}, status=status.HTTP_400_BAD_REQUEST)

        company.administrators.add(user)

        return Response({'success': True}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_admin(self, request, pk):
        """查询企业管理员"""
        company = self.get_object()
        admin = company.admin  # 获取企业的管理员
        admin_data = {
            'id': admin.id,
            'username': admin.username,
        }
        return Response(admin_data)

    @action(detail=True, methods=['get'])
    def get_administrators(self, request, pk):
        """查询企业所有团队管理员"""
        company = self.get_object()  # 获取特定的企业实例
        administrators = company.administrators.all()  # 获取企业的所有团队管理员
        administrators_data = [
            {
                'id': admin.id,
                'username': admin.username,
            }
            for admin in administrators
        ]
        return Response(administrators_data)

    @action(detail=True, methods=['get'])
    def get_teams(self, request, pk):
        """查询企业所有团队"""
        company = self.get_object()  # 获取特定的企业实例
        teams = company.teams.all()  # 获取企业的所有团队
        teams_data = [
            {
                'team_detail': TeamSerializer(team).data,
                'members': UserSerializer(team.users.all(), many=True).data,
            }
            for team in teams
        ]
        return Response(teams_data)

    def get_teams_short(self, request, pk):
        company = self.get_object()  # 获取特定的企业实例
        teams = company.teams.all()  # 获取企业的所有团队
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_users(self, request, pk):
        company = self.get_object()
        users = company.users.all()
        users_data = [
            {
                'id': user.id,
                'name': user.username,
            }
            for user in users
        ]
        return Response(users_data)

    @action(detail=True, methods=['get'])
    def get_detail(self, request, pk):
        company = self.get_object()
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        company = self.get_object()
        if not company:
            return Response({'error': '没有该企业'}, status=403)
        if company.admin.id != request.user.id:
            return Response({'error': '无权'}, status=400)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)