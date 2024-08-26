import uuid

import jieba
from django.core.files.base import ContentFile
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.companies.models import Company
from apps.documents.models import Template, Document, DocVersion, DocLog, Keyword
from apps.documents.serializers import TemplateSerializer, DocumentSerializer, InnerFileSerializer, \
    DocVersionSerializer, DocLogSerializer
from apps.teams.models import Team
from apps.users.models import User
from apps.users.permissions import SuperUserPermission, UserPermission
from common.utils import has_permission_for_document
from intelli.keyword.keyword import get_keywords


# Create your views here.


class TemplateViewSet(ModelViewSet):
    """模板相关视图集"""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]  # 只有超级管理员可以操作
    pagination_class = None

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')
        content = request.data.get('content')
        is_public = request.data.get('is_public')
        avatar = request.data.get('avatar')

        if not all([name, content]):
            return Response({'error': '参数不全'}, status=status.HTTP_400_BAD_REQUEST)

        # if is_public and not request.user.is_superuser:
        #     return Response({'error': '无权上传公共文档'}, status=status.HTTP_400_BAD_REQUEST)

        # 生成 .css 文件
        file_content = ContentFile(content.encode('utf-8'))
        unique_filename = f"{uuid.uuid4()}.css"

        template_instance = Template(
            name=name,
            description=description,
            user=request.user,
            is_public=True,
            avatar=avatar
        )
        template_instance.content.save(unique_filename, file_content)

        serializer = self.get_serializer(template_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def query_public(self, request, *args, **kwargs):
        templates = Template.objects.filter(is_public=True)
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def query_private(self, request, *args, **kwargs):
        templates = Template.objects.filter(is_public=False, user=request.user.id)
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        template = self.get_object()
        if not template:
            return Response({'error': '没有该模板'}, status=status.HTTP_400_BAD_REQUEST)

        if template.user.id != request.user.id:
            return Response({'error': '无权修改'}, status=status.HTTP_400_BAD_REQUEST)

        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kewargs):
        template = self.get_object()
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({'error': '缺少参数'}, status=400)
        template.avatar = avatar
        template.save()
        return Response({'success': 'yes'})


class DocumentView(APIView):
    """创建文件视图"""
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        creator_id = request.user.id
        owner = request.data.get('owner')

        # 检查参数是否完整
        if not all([name, owner]):
            return Response({'error': '参数不全'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查owner参数合法性
        try:
            owner = int(owner)
        except ValueError:
            return Response({'error':'owner参数必须为整数'}, status=status.HTTP_400_BAD_REQUEST)

        model_data = {
            'name': name,
            'owner': owner,
            'creator': creator_id,
        }
        if description:
            model_data['description'] = description
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            if avatar.size > 10 * 1024 * 1024:
                return Response({'error':'图像过大'}, status=status.HTTP_400_BAD_REQUEST)
            model_data['avatar'] = avatar

        # 将模板传入
        template = request.data.get('template')
        if template:
            try:
            
                model_data['template_id'] = int(template)
            except:
                pass

        owner_id = None
        # 检查文件owner是否合法
        if owner == 1:
            user = User.objects.get(id=creator_id)
            if not user:
                return Response({'error':'用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
            model_data['user'] = creator_id
            owner_id = creator_id
        elif owner == 2:
            owner_id = request.data.get('owner_id')
            if not owner_id:
                return Response({'error': '缺少owner_id参数'}, status=status.HTTP_400_BAD_REQUEST)

            team = get_object_or_404(Team, id=owner_id)
            if not team.users.filter(id=request.user.id).exists():
                return Response({'error': '该用户对该团队无权限'}, status=status.HTTP_400_BAD_REQUEST)
            model_data['team'] = owner_id
        elif owner == 3:
            owner_id = request.data.get('owner_id')
            if not owner_id:
                return Response({'error': '缺少owner_id参数'}, status=status.HTTP_400_BAD_REQUEST)

            company = get_object_or_404(Company, id=owner_id)
            if company.admin.id != request.user.id and not company.administrators.filter(id=request.user.id).exists():
                return Response({'error': '该用户不是企业管理者，无权进行此操作'}, status=status.HTTP_400_BAD_REQUEST)
            model_data['company'] = owner_id
        else:
            return Response({'error': 'owner参数非法'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DocumentSerializer(data=model_data)

        if serializer.is_valid():
            document = serializer.save()

            if int(template) == 2:
                k = Keyword.objects.filter(name='技术').first()
                document.keywords.add(k)
            elif int(template) == 3:
                k = Keyword.objects.filter(name='记录').first()
                document.keywords.add(k)
                k = Keyword.objects.filter(name='博客').first()
                document.keywords.add(k)
                k = Keyword.objects.filter(name='分享').first()
                document.keywords.add(k)
            elif int(template) == 4:
                k = Keyword.objects.filter(name='软件').first()
                document.keywords.add(k)
                k = Keyword.objects.filter(name='说明书').first()
                document.keywords.add(k)
                k = Keyword.objects.filter(name='开发').first()
                document.keywords.add(k)

            with transaction.atomic():
                ver_serializer = DocVersionSerializer(data={
                    'document': document.id,
                    'version': document.version_counts + 1,
                    'description': '版本一'
                })
                ver_serializer.is_valid(raise_exception=True)
                ver_serializer.save()
                document.version_counts += 1
                document.save(update_fields=['version_counts'])

            # 记录日志
            DocLog.objects.create(
                user=request.user,
                action=1,  # 对应创建文档
                document_type=owner,
                document_id=serializer.instance.id,
                owner_id=owner_id
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        document = Document.objects.filter(pk=pk).first()
        if not document:
            return Response({'error':'未找到该文档'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DocumentSerializer(document, data=request.data, partial=True)

        user = request.user
        if not has_permission_for_document(user, document):
            return Response({'error':'无权编辑该文档'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                document.avatar = avatar
            serializer.save()

            # 记录日志
            DocLog.objects.create(
                user=request.user,
                action=2,  # 对应更新文档
                document_type=document.owner,
                document_id=document.id,
                owner_id=document.user_id if document.owner == 1 else document.team_id if document.owner == 2 else document.company_id
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        team_id = request.query_params.get('team_id')
        company_id = request.query_params.get('company_id')

        documents = Document.objects.all()

        if user_id:
            documents = documents.filter(user_id=user_id)
        elif team_id:
            documents = documents.filter(team_id=team_id)
        elif company_id:
            documents = documents.filter(company_id=company_id)
        else:
            return Response({'error': 'Please provide a valid user_id, team_id or company_id'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = request.user
        document = Document.objects.filter(id=pk).first()
        if not document:
            return Response({'error': '没有该文档'}, status=status.HTTP_400_BAD_REQUEST)

        if document.user.id != user.id:
            return Response({'error': '无权操作'})

        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def update_keywords(self, request, pk):
        document = self.get_object()
        if not document:
            return Response({'error': '未找到该文档'}, status=status.HTTP_400_BAD_REQUEST)
        content = request.data.get('content')
        title = request.data.get('title')
        if not content or not title:
            return Response({'error': '缺少参数'}, status=status.HTTP_400_BAD_REQUEST)

        keywords = get_keywords(content, title)['items']
        res = []
        for tmp in keywords:
            keyword = tmp['tag']
            res.append(keyword)
            word_obj = Keyword.objects.filter(name=keyword).first()
            if word_obj:
                document.keywords.add(word_obj)
            else:
                obj = Keyword.objects.create(name=keyword)
                document.keywords.add(obj)
        return Response({'keywords': res})

    def search(self, request, *args, **kwargs):
        search_term = request.query_params.get('search', None)
        if not search_term:
            return Response({"error": "Search term is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # 对搜索词进行中文分词和英文分词
        search_terms = jieba.lcut_for_search(search_term)

        queries = Q()
        for term in search_terms:
            queries |= Q(keywords__name__icontains=term) | Q(name__icontains=term) | Q(description__icontains=term)

        documents = Document.objects.filter(
            owner=1,
            user=user
        ).filter(queries).distinct()[:10]  # 返回相对精准的前10个文档

        serializer = DocumentSerializer(documents, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def query(self, request, pk):
        document = Document.objects.filter(id=pk).first()
        if not document:
            return Response({'error': '未找到该文档'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentCollectView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def post(self, request):
        doc_id = request.data.get('doc_id')
        if not doc_id:
            return Response({'error': '缺少doc_id参数'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        document = Document.objects.filter(id=doc_id).first()
        if not document:
            return Response({'error': '没有该文档'}, status=status.HTTP_400_BAD_REQUEST)

        if ((document.owner == 1 and document.user != user) or
                (document.owner == 2 and not document.team.users.filter(id=user.id).exists()) or
                (document.owner == 3 and not document.company.users.filter(id=user.id).exists())):
            return Response({'error': '无权收藏该文档'}, status=status.HTTP_400_BAD_REQUEST)

        if user.collect_documents.filter(id=doc_id).exists():
            user.collect_documents.remove(doc_id)
        else:
            user.collect_documents.add(document)
        return Response({'data': 'success'}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        documents = Document.objects.filter(collect_users=user)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocVersionView(APIView):
    """创建新版本视图"""
    permission_classes = [IsAuthenticated, UserPermission]
    pagination_class = None

    def post(self, request):
        user = request.user
        document_id = request.data.get('document_id')
        source_version = request.data.get('source_version')
        description = request.data.get('description')

        if not document_id or source_version is None:
            return Response({'error': '参数不全'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source_version = int(source_version)
            document_id = int(document_id)
        except ValueError:
            return Response({'error':'参数不合法'}, status=status.HTTP_400_BAD_REQUEST)

        document = get_object_or_404(Document, id=document_id)
        if not has_permission_for_document(user, document):
            return Response({'error':'无权操作该文档'}, status=status.HTTP_400_BAD_REQUEST)

        if source_version == 0:
            serializer = DocVersionSerializer(data={
                'document': document_id,
                'version': document.version_counts + 1,
                'source_version': source_version,
                'description': description
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            with transaction.atomic():
                doc = Document.objects.select_for_update().get(id=document.id)
                doc.version_counts += 1
                doc.save(update_fields=['version_counts'])

            # 记录日志
            DocLog.objects.create(
                user=request.user,
                action=4,  # 对应新建文档版本
                document_type=document.owner,
                document_id=document.id,
                version_id=serializer.instance.id,
                owner_id=document.user_id if document.owner == 1 else document.team_id if document.owner == 2 else document.company_id
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not document.versions.filter(version=source_version).exists():
                return Response({'error':'原版本不存在'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = DocVersionSerializer(data={
                'content': document.versions.filter(version=source_version).first().content,
                'document': document_id,
                'version': document.version_counts + 1,
                'source_version': source_version,
                'description': description
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            with transaction.atomic():
                doc = Document.objects.select_for_update().get(id=document.id)
                doc.version_counts += 1
                doc.save(update_fields=['version_counts'])

            # 记录日志
            DocLog.objects.create(
                user=request.user,
                action=4,  # 对应新建文档版本
                document_type=document.owner,
                document_id=document.id,
                version_id=serializer.instance.id,
                owner_id=document.user_id if document.owner == 1 else document.team_id if document.owner == 2 else document.company_id
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        user = request.user
        content = request.data.get('content')
        document_id = request.data.get('document_id')
        description = request.data.get('description')

        if not document_id:
            return Response({'error':'参数不全'}, status=status.HTTP_400_BAD_REQUEST)

        document = get_object_or_404(Document, id=document_id)
        if not has_permission_for_document(user, document):
            return Response({'error':'无权操作该文档'}, status=status.HTTP_400_BAD_REQUEST)

        version = get_object_or_404(document.versions, version=pk)
        val_data = {
            'content': content
        }
        if description:
            val_data['description'] = description
        serializer = DocVersionSerializer(version, data=val_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 记录日志
        DocLog.objects.create(
            user=request.user,
            action=5,  # 对应更新某个版本
            document_type=document.owner,
            document_id=document.id,
            version_id=version.id,
            owner_id=document.user_id if document.owner == 1 else document.team_id if document.owner == 2 else document.company_id
        )

        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        document_id = request.query_params.get('document_id')

        if not document_id:
            return Response({'error': 'Please provide a valid document_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        doc_versions = DocVersion.objects.filter(document=document)
        serializer = DocVersionSerializer(doc_versions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = request.user
        version = DocVersion.objects.filter(id=pk).first()
        if not version:
            return Response({'error': '没有该版本'}, status=400)

        # todo 鉴权
        version.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InnerFileCreateView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    def post(self, request):
        # 检查上传的文件里是否有content字段
        if 'file' not in request.FILES:
            return Response({'error': '上传的文件没有file字段'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查文件大小，此处设定不超过10MB
        content = request.FILES['file']
        if content.size > 1024 * 1024 * 10:
            return Response({'error': '文件过大'}, status=status.HTTP_400_BAD_REQUEST)

        affiliated_document_id = request.data.get('affiliated_document_id')
        if not affiliated_document_id:
            return Response({'error':'缺少affiliated_document_id参数'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        document = get_object_or_404(Document, id=affiliated_document_id)

        if not has_permission_for_document(user, document):
            return Response({'error':'无权编辑该文档'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InnerFileSerializer(data={
            'file':content,
            'affiliated_document':affiliated_document_id,
            'user': user.id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DocLogView(APIView):
    """日志视图"""
    permission_classes = [IsAuthenticated]
    # pagination_class = None

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        team_id = request.query_params.get('team_id')
        company_id = request.query_params.get('company_id')

        logs = DocLog.objects.all()

        if user_id:
            if int(user_id) != request.user.id:
                return Response({'error': '无权进行此查询'}, status=status.HTTP_400_BAD_REQUEST)
            logs = logs.filter(owner_id=user_id, document_type=1)
        elif team_id:
            team = Team.objects.filter(id=int(team_id)).first()
            if not team:
                return Response({'error': '没有该团队'}, status=status.HTTP_400_BAD_REQUEST)
            if not team.users.filter(id=request.user.id).exists():
                return Response({'error': '无权进行此查询'}, status=status.HTTP_400_BAD_REQUEST)
            logs = logs.filter(owner_id=team_id, document_type=2)
        elif company_id:
            company = Company.objects.filter(id=int(company_id)).first()
            if not company:
                return Response({'error': '没有该企业'}, status=status.HTTP_400_BAD_REQUEST)
            if not company.users.filter(id=request.user.id).exists():
                return Response({'error': '无权进行此查询'}, status=status.HTTP_400_BAD_REQUEST)
            logs = logs.filter(owner_id=company_id, document_type=3)
        else:
            return Response({'error': 'Please provide a valid user_id, team_id or company_id'}, status=status.HTTP_400_BAD_REQUEST)

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(logs, request)
        if page is not None:
            serializer = DocLogSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = DocLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)