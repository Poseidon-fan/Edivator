import os
import random
import uuid
from PIL import Image

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
from apps.documents.models import Document, Keyword
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from common.utils import check_is_all
from apps.users.models import User
from .serializer import UserSerializer
from .permissions import UserPermission
from ..companies.models import Company
from ..invitations.models import Invitation
from ..teams.models import Notification


# Create your views here.


class LoginView(TokenObtainPairView):
    """登录视图"""
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # 自定义登录成功返回的结果
        result = serializer.validated_data
        result['id'] = serializer.user.id
        result['mobile'] = serializer.user.mobile
        result['email'] = serializer.user.email
        result['username'] = serializer.user.username
        result['point'] = serializer.user.point
        if serializer.user.avatar:
            result['avatar'] = serializer.user.avatar.url
        else:
            result['avatar'] = None

        result['token'] = result.pop('access')

        return Response(result, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """注册视图"""
    def post(self, request):
        # 1.接受用户参数
        username = request.data.get('username')  # 用户名
        password = request.data.get('password')  # 密码
        email = request.data.get('email')  # 邮箱
        if not check_is_all([username, password, email]):
            return Response({'error': '参数错误'}, status=status.HTTP_400_BAD_REQUEST)

        # TODO 参数校验

        # 3.创建用户
        try:
            obj = User.objects.create_user(username=username, password=password, email=email)
        except:
            return Response({'error': '已有同名用户'}, status=status.HTTP_400_BAD_REQUEST)
        # 4. 增加默认通知
        Notification.objects.create(user=obj, message='欢迎来到Edivator')
        # 5. 创建默认企业
        company = Company.objects.create(name=username + '的企业', admin=obj, description='默认创建的企业')
        company.users.add(obj)
        company.administrators.add(obj)

        res = {
            'username': obj.username,
            'id': obj.id,
            'email': obj.email,
        }

        return Response(res, status=status.HTTP_201_CREATED)


class UserView(GenericViewSet, mixins.RetrieveModelMixin):
    """用户相关操作视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]  # 设置认证用户才有访问权限，且防止越权
    pagination_class = None

    def recharge(self, request, *args, **kwargs):
        """重置"""
        point = request.data.get('point')
        request.user.point += int(point)
        request.user.save()
        return Response({'res': '重置成功', 'cur_point': request.user.point}, status=200)

    def upload_avatar(self, request, *args, **kwargs):
        """上传头像"""
        avatar = request.data.get('avatar')
        # 校验是否上传了文件
        if not avatar:
            return Response({'error':'上传失败，文件不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验文件大小不能超过300kb
        if avatar.size > 2097152:
            return Response({'error':'上传失败，文件大小不能超过300kb'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 重命名文件
        user = self.get_object()
        file_extension = os.path.splitext(avatar.name)[1]  # 获取文件扩展名
        new_filename = uuid.uuid4().hex + file_extension

        # 打开图像文件并保存
        img = Image.open(avatar)
        file_path = os.path.join('user_avatars/', new_filename)  # 文件保存路径
        temp_file = ContentFile(b'')  # 创建一个临时文件对象
        img.save(temp_file, format=img.format)  # 保存图像到临时文件对象
        temp_file.seek(0)  # 重置文件指针到开始位置
        saved_path = default_storage.save(file_path, temp_file)  # 保存文件到默认存储

        # 更新用户的 avatar 字段
        user.avatar = saved_path
        user.save()

        return Response({'url': saved_path}, status=status.HTTP_200_OK)

    def join_company(self, request, *args, **kwargs):
        token = request.data.get('token')
        company_name = request.data.get('company_name')
        # 检查上传的参数
        if not token or not company_name:
            return Response({'error':'缺少必要的参数'}, status=status.HTTP_400_BAD_REQUEST)

        # 校验验证码存在性
        invitation = Invitation.objects.filter(token=token, user_id=request.user.id).first()
        if not invitation:
            return Response({'error':'邀请码无效'}, status=status.HTTP_400_BAD_REQUEST)

        # 校验验证码合法性
        if invitation.company.name != company_name:
            return Response({'error':'邀请码无效'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查日期合法性
        if invitation.expires_at < timezone.now():
            return Response({'error':'邀请码过期'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查邀请码是否已经被使用
        if invitation.is_accepted:
            return Response({'error':'邀请码已被使用'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查用户是否已经加入企业
        company = Company.objects.get(name=company_name)

        if company.users.filter(id=request.user.id).exists():
            return Response({'error':'用户已经在该企业中'}, status=status.HTTP_400_BAD_REQUEST)

        # 加入企业
        company.users.add(request.user)
        invitation.is_accepted = True
        invitation.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_detail(self, request):
        user = request.user
        user_data = self.get_serializer(user).data
        companies = Company.objects.filter(users=user)
        company_ids = [company.id for company in companies]
        user_data['company_ids'] = list(company_ids)

        documents = Document.objects.filter(user=user, owner=1)
        keywords = Keyword.objects.filter(documents__in=documents).distinct()
        keyword_list = list(keywords.values_list('name', flat=True))
        keywords = []
        for keyword in keyword_list:
            keywords.append([keyword, random.randint(1, 10)])
        user_data['keywords'] = keywords
        
        return Response(user_data)

    def get_doc_nums(self, request):
        user = request.user
        # 获取个人文档数量
        personal_document_count = Document.objects.filter(user=user, owner=1).count()

        # 获取团队文档数量
        team_ids = user.affiliated_teams.values_list('id', flat=True)
        team_document_count = Document.objects.filter(team__id__in=team_ids, owner=2).count()

        # 获取企业文档数量
        company_ids = user.affiliated_companies.values_list('id', flat=True)
        company_document_count = Document.objects.filter(company__id__in=company_ids, owner=3).count()

        return Response({
            'personal_document_count': personal_document_count,
            'team_document_count': team_document_count,
            'company_document_count': company_document_count,
            'total_count': personal_document_count + team_document_count + company_document_count
        })


