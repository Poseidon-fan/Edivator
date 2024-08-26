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

from apps.documents import views

urlpatterns = [
    # 创建模板
    path('templates/create/', views.TemplateViewSet.as_view({'post':'create'})),
    # 查询公共模板
    path('templates/query_public/', views.TemplateViewSet.as_view({'get':'query_public'})),
    # 查询私有模板
    path('templates/query_private/', views.TemplateViewSet.as_view({'get':'query_private'})),
    # 删除模板
    path('templates/delete/<int:pk>/', views.TemplateViewSet.as_view({'delete': 'destroy'})),
    # 更新文档图片
    path('templates/update/<int:pk>/', views.TemplateViewSet.as_view({'put': 'update'})),
    # 创建文档
    path('create/', views.DocumentView.as_view()),
    # 更新文档
    path('update/<int:pk>/', views.DocumentView.as_view()),
    # 删除文档
    path('delete/<int:pk>/', views.DocumentView.as_view()),
    # 创建版本
    path('versions/create/', views.DocVersionView.as_view()),
    # 更新版本的内容
    path('versions/update/<int:pk>/', views.DocVersionView.as_view()),
    # 删除版本
    path('versions/delete/<int:pk>/', views.DocVersionView.as_view()),
    # 上传文档中的文件
    path('inner_files/create/', views.InnerFileCreateView.as_view()),
    # 查询文档
    path('query_doc/', views.DocumentView.as_view()),
    #查询单个文档
    path('query_single_doc/<int:pk>/', views.DocumentViewSet.as_view({'get':'query'})),
    # 查询文档版本
    path('query_version/', views.DocVersionView.as_view()),
    # 查询文档日志
    path('query_logs/', views.DocLogView.as_view()),
    # 收藏文档
    path('collects/do/', views.DocumentCollectView.as_view()),
    # 获取所有的收藏文档
    path('collects/query/', views.DocumentCollectView.as_view()),
    # 更新文档关键词
    path('update_keywords/<int:pk>/', views.DocumentViewSet.as_view({'put': 'update_keywords'})),
    # 根据关键词搜索
    path('search_by_keyword/', views.DocumentViewSet.as_view({'get': 'search'})),
]
