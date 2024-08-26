from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.models import Company
from apps.teams.models import Team, Message, Notification
from apps.teams.serializer import TeamSerializer, MessageSerializer, NotificationSerializer
from apps.users.models import User
from apps.users.permissions import UserPermission
from apps.users.serializer import UserSerializer
from common.utils import check_is_all


# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    """团队视图"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 确保数据有效
        serializer.is_valid(raise_exception=True)

        admin_id = request.user.id
        company_id = request.data.get('company_id')
        if not check_is_all([admin_id, company_id]):
            return Response({'error': '提交数据缺失'}, status=status.HTTP_400_BAD_REQUEST)

        # 校验admin_id 和 company_id是否匹配
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({'error': '公司不存在'}, status=status.HTTP_400_BAD_REQUEST)

        if not company.administrators.filter(id=admin_id).exists():
            return Response({'error': '用户无权进行此操作'}, status=status.HTTP_400_BAD_REQUEST)

        # 校验该团队是否已经在企业中被创建了
        name = request.data.get('name')
        if company.teams.filter(name=name).exists():
            return Response({'error': '该企业中已有这个名字的团队了'}, status=status.HTTP_400_BAD_REQUEST)

        team = serializer.save()
        team.users.add(request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def add_user(self, request, *args, **kwargs):
        """拉人进入团队"""
        company_id = request.data.get('company_id')
        team_name = request.data.get('team_name')
        user_id = request.data.get('user_id')

        # 校验参数是否缺失
        if not check_is_all([company_id, team_name, user_id]):
            return Response({'error':'缺少参数'}, status=status.HTTP_400_BAD_REQUEST)

        admin = User.objects.get(id=request.user.id)
        company = Company.objects.filter(id=company_id).first()
        user = User.objects.filter(id=user_id).first()
        team = Team.objects.filter(name=team_name).first()

        # 校验数据库中是否已经有三条记录
        if not admin or not user or not company or not team:
            return Response({'error':'参数错误'}, status=status.HTTP_400_BAD_REQUEST)

        # 校验操作者是否为企业拥有者
        if company.admin != admin and not company.administrators.filter(id=request.user.id).exists():
            return Response({'error':'非企业管理者无权进行此操作'}, status=status.HTTP_400_BAD_REQUEST)

        # 查看用户是否在企业中
        if not company.users.filter(id=user_id).exists() and company.admin.id != user_id:
            return Response({'error': '用户不在该企业中'}, status=status.HTTP_400_BAD_REQUEST)

        # 检验团队是否为企业的团队
        if not company.teams.filter(id=team.id).exists():
            return Response({'error': '企业中没有该团队'}, status=status.HTTP_400_BAD_REQUEST)

        # 检验该用户是否已经在团队里
        if team.users.filter(id=user_id).exists():
            return Response({'error': '用户已在团队里'}, status=status.HTTP_400_BAD_REQUEST)

        # 加入团队
        team.users.add(user)

        return Response(status=status.HTTP_200_OK)

    def get_users(self, request, pk):
        team = self.get_object()
        users = team.users.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def get_detail(self, request, pk):
        team = self.get_object()
        serializer = self.get_serializer(team)
        return Response(serializer.data)

    # 获取用户所在的企业里所在的所有团队
    def get_user_company_teams(self, request):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({'error': '缺少company_id参数'}, status=status.HTTP_400_BAD_REQUEST)

        company = Company.objects.filter(id=company_id).first()

        # 判断是否有该企业
        if not company:
            return Response({'error': '查询不到该企业'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断用户是否在企业里
        if not company.users.filter(id=request.user.id).exists():
            return Response({'error': '用户不在该企业中'}, status=status.HTTP_400_BAD_REQUEST)

        teams = company.teams.filter(users=request.user).all()
        res_data = [
            {
                'team_detail': TeamSerializer(team).data,
                'members': UserSerializer(team.users.all(), many=True).data
            }
            for team in teams
        ]
        return Response(res_data)

    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        if not team.company.administrators.filter(id=request.user.id).exists():
            return Response({'error': '无权进行该操作'})
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def exit(self, request, *args, **kwargs):
        try:
            team = self.get_object()
        except:
            return Response({'error': '没有该团队'}, status=status.HTTP_400_BAD_REQUEST)
        if not team:
            return Response({'error': '没有该团队'}, status=status.HTTP_400_BAD_REQUEST)

        if not team.users.filter(id=request.user.id).exists():
            return Response({'error': '无法退出不在的团队'}, status=status.HTTP_400_BAD_REQUEST)

        team.users.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def create(self, request, *args, **kwargs):
            data = request.data.copy()
            data['applicant'] = request.user.id

            team_id = data.get('team')
            if not team_id:
                raise ValidationError({'team': 'Team ID is required.'})

            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                raise ValidationError({'team': 'Team does not exist.'})

            # 校验用户是否在企业里
            company_users = team.company.users.all()
            if request.user not in company_users:
                raise ValidationError({'detail': 'You can only apply to join teams within your own company.'})

            # 校验用户是否已经在团队里
            if request.user in team.users.all():
                raise ValidationError({'detail': 'You are already a member of this team.'})

            # 校验是否已存在未处理的申请
            existing_request = Message.objects.filter(applicant=request.user, team=team, status='pending').exists()
            if existing_request:
                raise ValidationError({'detail': 'You have already sent a pending request to join this team.'})

            # 默认消息状态为pending
            data['status'] = 'pending'

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            res = serializer.data
            res['user_name'] = request.user.username
            res['team_name'] = team.name
            return Response(res, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        message = self.get_object()

        # 校验是否为管理员
        if request.user not in message.team.company.administrators.all():
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        # 校验消息状态是否为pending
        if message.status != 'pending':
            return Response({'detail': 'This request has already been processed.'}, status=status.HTTP_400_BAD_REQUEST)

        message.status = 'approved'
        message.save()
        message.team.users.add(message.applicant)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        message = self.get_object()

        # 校验是否为管理员
        if request.user not in message.team.company.administrators.all():
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        # 校验消息状态是否为pending
        if message.status != 'pending':
            return Response({'detail': 'This request has already been processed.'}, status=status.HTTP_400_BAD_REQUEST)

        message.status = 'rejected'
        message.save()
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_requests(self, request, company_id=None):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({'detail': 'Company ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'detail': 'Company does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(applicant=request.user.id, team__company=company)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending_requests(self, request, company_id=None):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return Response({'detail': 'Company ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'detail': 'Company does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in company.administrators.all():
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(team__company=company, status='pending')
        res = [
            {
                'message': MessageSerializer(message).data,
                'user_name': message.applicant.username,
                'team_name': message.team.name
            }
            for message in messages
        ]

        return Response(res)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request):
        notification_ids = request.data.get('ids', [])
        if not notification_ids:
            return Response({'detail': 'No notification IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        notifications = Notification.objects.filter(id__in=notification_ids, user=request.user)
        notifications.update(is_read=True)
        return Response({'status': 'marked as read'}, status=status.HTTP_200_OK)