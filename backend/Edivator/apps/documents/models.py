from django.db import models

from apps.companies.models import Company
from apps.teams.models import Team
from apps.users.models import User
from common.db import BaseModel


# Create your models here.


class Template(BaseModel):
    """文档模板模型"""
    name = models.CharField(max_length=20, verbose_name='模板名')
    description = models.CharField(max_length=255, blank=True, null=True)
    content = models.FileField(upload_to='templates/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='template_avatars/', blank=True, null=True)

    class Meta:
        db_table = 'templates'
        verbose_name = '模板'
        verbose_name_plural = '模板列表'


class Keyword(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='关键词')

    def __str__(self):
        return str(self.id) + " " + self.name

    class Meta:
        db_table = 'keywords'


class Document(BaseModel):
    """文档基础信息模型（同一份文档的公共字段）"""
    name = models.CharField(max_length=100, verbose_name='文档')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='文档描述')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_documents', verbose_name='创建者')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', null=True, blank=True,
                             verbose_name='所属个人')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='documents', null=True, blank=True,
                             verbose_name='所属团队')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents', null=True, blank=True,
                                verbose_name='所属企业')

    template = models.ForeignKey(Template, on_delete=models.SET_NULL, related_name='documents', null=True, blank=True,
                                 verbose_name='文档模板')

    owner_choices = (
        (1, '个人'),
        (2, '团队'),
        (3, '企业'),
    )

    owner = models.IntegerField(choices=owner_choices, verbose_name='文档所属者类型')
    avatar = models.ImageField(upload_to='doc_avatars', null=True, blank=True, verbose_name='文档头像')
    version_counts = models.IntegerField(default=0, verbose_name='版本号分配')
    collect_users = models.ManyToManyField(User, related_name='collect_documents', blank=True, verbose_name='收藏的用户')
    keywords = models.ManyToManyField(Keyword, related_name='documents')

    class Meta:
        db_table = 'documents'
        verbose_name = '文档'
        verbose_name_plural = '文档列表'


class DocVersion(BaseModel):
    content = models.TextField(verbose_name='文档内容', null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='版本说明')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions', null=True, blank=True, verbose_name='所属文档')
    version = models.IntegerField(default=1, verbose_name='版本号')
    source_version = models.IntegerField(default=0, verbose_name='源于哪个版本')

    class Meta:
        db_table = 'doc_versions'
        verbose_name = '文档版本'
        verbose_name_plural = '文档版本列表'


class InnerFile(BaseModel):
    """文档中的文件元素"""
    file = models.FileField(upload_to='inner_files', verbose_name='文档中的文件')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inner_files', verbose_name='属于哪个用户')
    affiliated_document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='inner_files', verbose_name='基于哪个文档上传的')

    class Meta:
        db_table = 'inner_files'
        verbose_name = '文档中文件'
        verbose_name_plural = '文档中文件列表'


class DocLog(models.Model):
    OPERATION_CHOICES = [
        (1, '创建文档'),
        (2, '更新文档'),
        (3, '删除文档'),
        (4, '新建文档版本'),
        (5, '更新某个版本'),
        (6, '删除某个版本'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        (1, '个人'),
        (2, '团队'),
        (3, '企业'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='操作用户')
    time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    action = models.IntegerField(choices=OPERATION_CHOICES, verbose_name='操作类型')
    document_type = models.IntegerField(choices=DOCUMENT_TYPE_CHOICES, verbose_name='文档类型')
    document_id = models.IntegerField(verbose_name='文档ID')
    version_id = models.IntegerField(null=True, blank=True, verbose_name='版本ID')

    # 记录文档所属对象ID
    owner_id = models.IntegerField(verbose_name='所有者ID')

    class Meta:
        db_table = 'dco_log'
        verbose_name = '日志'
        verbose_name_plural = '日志'


