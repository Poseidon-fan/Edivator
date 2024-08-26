from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.chat.models import ChatMessage
from apps.chat.serializers import ChatMessageSerializer
from apps.teams.models import Team


# Create your views here.


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def query(self, request, *args, **kwargs):
        group_id = request.query_params.get('group_id', None)
        if group_id is None:
            return Response({'error': '缺少group_id参数'}, status=status.HTTP_400_BAD_REQUEST)

        group = Team.objects.filter(id=group_id).first()
        if not group:
            return Response({'error': '没有该群组'}, status=status.HTTP_400_BAD_REQUEST)

        messages = ChatMessage.objects.filter(team=group)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
