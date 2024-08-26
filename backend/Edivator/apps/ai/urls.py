"""
URL configuration for Edivator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import AiChatViewSet, OcrViewSet, DialogViewSet, WordStylesView, PictureViewSet, SpeechViewSet

urlpatterns = [
    path('chat/summarize/', AiChatViewSet.as_view({'post': 'summarize'})),
    path('chat/translate/', AiChatViewSet.as_view({'post': 'translate'})),
    path('chat/polish/', AiChatViewSet.as_view({'post': 'polish'})),
    path('chat/continue_write/',
         AiChatViewSet.as_view({'post': 'continue_write'})),
    path('chat/common_chat/', AiChatViewSet.as_view({'post': 'common_chat'})),
    path('chat/form/', AiChatViewSet.as_view({'post': 'form'})),
    # 文字识别
    path('ocr/infer/', OcrViewSet.as_view({'post': 'ocr_pic'})),
    # 模式识别
    path('ocr/pattern/', OcrViewSet.as_view({'post': 'ocr_pattern'})),

    path('correct/', AiChatViewSet.as_view({'post': 'correct'})),

    path('chat/styled_ggenerate/', AiChatViewSet.as_view({'post': 'styled_generate'})),

    # 生成图片
    path('pictures/generate/', PictureViewSet.as_view({'post': 'generate'})),
    # 获取图片
    path('pictures/get_img/', PictureViewSet.as_view({'post': 'query'})),

    # 增加对话记录
    path('dialogs/create/', DialogViewSet.as_view({'post': 'create'})),

    # 查询用户的历史聊天记录
    path('dialogs/query/', DialogViewSet.as_view({'get': 'list'})),
    # 提取样式
    path('extract_style/', WordStylesView.as_view()),

    # 语音提取
    path('speeches/recognize/', SpeechViewSet.as_view({'post': 'recognize'})),

    # 生成思维导图
    path('gen_mind/', AiChatViewSet.as_view({'post': 'gen_mind'})),
]
