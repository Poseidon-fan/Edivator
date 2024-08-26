import json
import os
import tempfile
import uuid
import time
from urllib.parse import quote

from intelli.mind.mind import gen_mind
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Edivator.settings import MEDIA_ROOT
from apps.ai.models import Dialog
from apps.ai.serializers import DialogSerializer
from apps.users.models import User
from intelli.ocr.ocr_bot import OCRbot
from intelli.chat.chatbot import ChatBot
from rest_framework.permissions import AllowAny, IsAuthenticated

from intelli.pictures.picture_bot import generate, get_img
from intelli.speech.speech_bot import recognize
from intelli.style.extract import extract_styles_from_document, summarize_styles


class AiChatViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    chatbot = ChatBot()
    pagination_class = None

    @action(detail=False, methods=['post'])
    def form(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        res = self.chatbot.form(content)
        user.point -= 1
        user.save()
        return Response({'res': res})

    @action(detail=False, methods=['post'])
    def summarize(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        summary = self.chatbot.summarize(content)
        user.point -= 1
        user.save()
        return Response({'summary': summary})

    @action(detail=False, methods=['post'])
    def translate(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        language = request.data.get('language')
        if not language:
            return Response({'error': 'Language is required'}, status=400)
        translated = self.chatbot.translate(content, language)
        user.point -= 1
        user.save()
        return Response({'translated': translated})

    @action(detail=False, methods=['post'])
    def polish(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        polished = self.chatbot.polish(content)
        user.point -= 1
        user.save()
        return Response({'polished': polished})

    @action(detail=False, methods=['post'])
    def continue_write(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        continued = self.chatbot.continue_write(content)
        user.point -= 1
        user.save()
        return Response({'continued': continued})
    

    @action(detail=False, methods=['post'])
    def common_chat(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        response = self.chatbot.common_chat(content)
        user.point -= 1
        user.save()
        return Response({'response': response})

    @action(detail=False, methods=['post'])
    def correct(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        response = self.chatbot.correct(content)
        user.point -= 1
        user.save()
        return Response({'response': response})

    @action(detail=False, methods=['post'])
    def styled_generate(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        content = request.data.get('content')
        style = request.data.get('style')
        if not content or not style:
            return Response({'error': 'Content and style are required'}, status=400)
        response = self.chatbot.styled_generate(content, style)
        user.point -= 1
        user.save()
        return Response({'response': response})
    
    @action(detail=False, methods=['post'])
    def gen_mind(self, request):
        print(request.user.point)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required'}, status=400)
        try:
            res = gen_mind(content)
            return Response({'result': res}, status=200)
        except:
            return Response({'error': '生成失败'}, status=400)


class OcrViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    ocrbot = OCRbot()
    pagination_class = None

    @action(detail=False, methods=['post'])
    def ocr_pic(self, request):

        base64_img = request.data.get('base64_img')
        if not base64_img:
            return Response({'error': 'base64_img is required'}, status=400)
        try:
            result = self.ocrbot.infer_img_and_return(base64_img)
        except:
            return Response({'error': 'OCR failed'}, status=400)

        txts = result[1]
        image = result[0]
        relative_path = os.path.join('files', 'ocr_res')
        if not os.path.exists(relative_path):
            os.makedirs(relative_path)
        image_filename = uuid.uuid4().hex + '.jpg'
        image_path = os.path.join(relative_path, image_filename)
        image.save(image_path)

        image_url = request.build_absolute_uri('/' + image_path.replace('\\', '/'))

        return Response({
            'image_url': image_url,
            'texts': txts
        })

    @action(detail=False, methods=['post'])
    def ocr_pattern(self, request):

        base64_img = request.data.get('base64_img')
        if not base64_img:
            return Response({'error': 'base64_img is required'}, status=400)
        try:
            result = self.ocrbot.recognize_pattern(quote(base64_img))
        except:
            return Response({'error': 'OCR failed'}, status=400)

        return Response(result, status=200)


class DialogViewSet(ModelViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            queryset = self.queryset.filter(user=user)
            if not queryset.exists():
                # 插入一条欢迎信息
                welcome_dialog = Dialog.objects.create(
                    user=user,
                    text="你好，我是小 E！是Edivator的智能机器人，请问有什么我可以帮助您的",
                    sender='bot'
                )
                queryset = self.queryset.filter(user=user)  # 重新获取查询集，包含新插入的记录
        else:
            return Response({'error': 'user_id字段必填'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WordStylesView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        file = request.FILES.get('doc')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            # 提取样式
            styles_info = extract_styles_from_document(temp_file_path)
            summary = summarize_styles(styles_info)
        except Exception as e:
            print(e)
            return Response({'error': '提取失败'}, status=400)
        finally:
            # 删除临时文件
            os.remove(temp_file_path)
        permission_classes = [IsAuthenticated]

        return Response(summary, status=status.HTTP_200_OK)


class PictureViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def generate(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        text = request.data.get('text')
        resolution = request.data.get('resolution')
        style = request.data.get('style')

        if not text or not style:
            return Response({'error': '缺少参数'}, status=400)
        try:
            res = generate(text, resolution, style)
        except:
            return Response({'error': '生成错误'}, status=400)
        user.point -= 1
        user.save()
        return Response(json.loads(res), status=200)

    def query(self, request):
        taskId = request.data.get('taskId')
        res = json.loads(get_img(taskId))
        while res['data']['status'] != 1:
            time.sleep(2)
            res = json.loads(get_img(taskId))
        return Response({'img': res['data']['img']}, status=200)


class SpeechViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def recognize(self, request):
        user = request.user
        if user.point <= 0:
            return Response({'error': '账户余额不足'}, status=400)
        file_format = request.data.get('file_format')
        speech = request.data.get('speech')
        my_uuid = request.data.get('uuid')

        if not all([file_format, speech, my_uuid]):
            return Response({'error': '参数不全'}, status=400)
        dev_pid = 1537
        if request.data.get('dev_pid'):
            dev_pid = request.data.get('dev_pid')

        try:
            res = recognize(file_format, my_uuid, speech, dev_pid)
        except:
            return Response({'error': '识别失败'}, status=400)
        user.point -= 1
        user.save()
        return Response(json.loads(res), status=200)

    def query(self, request):
        taskId = request.data.get('taskId')
        res = get_img(taskId)
        return Response(json.loads(res), status=200)