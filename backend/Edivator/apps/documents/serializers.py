from rest_framework import serializers

from apps.companies.models import Company
from apps.documents.models import Document, InnerFile, Template, DocVersion, DocLog, Keyword
from apps.teams.models import Team

from apps.users.models import User
from apps.users.serializer import UserSerializer


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    """文档序列化容器"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), required=False, allow_null=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False, allow_null=True)
    template = TemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(source='template', queryset=Template.objects.all(),
                                                     write_only=True)
    keywords = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = '__all__'

    def get_keywords(self, obj):
        return [keyword.name for keyword in obj.keywords.all()]

    def get_template(self, obj):
        return TemplateSerializer(obj.template).data

    def validate(self, attrs):
        if not self.instance:
            # 当前是创建新记录
            # 检查user、team和company中是否至少有一个被设置了
            if all(value is None for value in [attrs.get('user'), attrs.get('team'), attrs.get('company')]):
                raise serializers.ValidationError("user，team，company参数必须指定一个")
        return attrs


    def update(self, instance, validated_data):
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'avatar' in validated_data:
            avatar = validated_data.pop('avatar')
            instance.avatar = avatar
        instance.save()
        return instance


class DocVersionSerializer(serializers.ModelSerializer):
    """文档版本序列化容器"""
    class Meta:
        model = DocVersion
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'content' in validated_data:
            instance.content = validated_data.get('content', instance.content)
        if 'description' in validated_data:
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class InnerFileSerializer(serializers.ModelSerializer):
    """文档中的文件序列化器"""
    affiliated_document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = InnerFile
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    """文档模板的序列化器"""

    class Meta:
        model = Template
        fields = '__all__'


class DocLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    document = serializers.SerializerMethodField()
    version = serializers.SerializerMethodField()

    class Meta:
        model = DocLog
        fields = ['id', 'user', 'time', 'action', 'document_type', 'owner_id', 'document', 'version']
        # 排除 document_id 和 version_id 字段
        # fields = ['id', 'user', 'time', 'action', 'document_type', 'owner_id', 'document', 'version']

    def get_document(self, obj):
        document = Document.objects.filter(id=obj.document_id).first()
        if document:
            return DocumentSerializer(document).data
        return None

    def get_version(self, obj):
        if obj.version_id:
            version = DocVersion.objects.filter(id=obj.version_id).first()
            if version:
                return DocVersionSerializer(version).data
        return None


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
