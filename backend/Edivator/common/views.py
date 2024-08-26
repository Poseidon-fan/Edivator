import os

from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Edivator.settings import MEDIA_ROOT


class FileView(APIView):
    """获取文件的视图"""
    def get(self, request, name):
        path = os.path.join(MEDIA_ROOT, name)
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error':"没有找到该文件"}, status=status.HTTP_404_NOT_FOUND)