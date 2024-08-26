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
from django.urls import path, include, re_path
from common.views import FileView

# from apps.files.views import AvatarGetView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('users/', include('apps.users.urls')),  # 用户
    path('companies/', include('apps.companies.urls')),  # 企业
    path('invitations/', include('apps.invitations.urls')),  # 邀请码
    path('teams/', include('apps.teams.urls')),  # 团队
    path('documents/', include('apps.documents.urls')),  # 文档
    path('ai/', include('apps.ai.urls')),  # AI功能
    re_path(r'^files/(?P<name>.*)$', FileView.as_view(), name='serve-file'),  # 获取静态文件
    path('api/users/', include('apps.users.urls')),  # 用户
    path('api/companies/', include('apps.companies.urls')),  # 企业
    path('api/invitations/', include('apps.invitations.urls')),  # 邀请码
    path('api/teams/', include('apps.teams.urls')),  # 团队
    path('api/documents/', include('apps.documents.urls')),  # 文档
    path('api/ai/', include('apps.ai.urls')),  # AI功能
    path('api/messages/', include('apps.chat.urls')),
    re_path(r'^files/(?P<name>.*)$', FileView.as_view(),
            name='serve-file'),  # 获取静态文件
    re_path(r'api/^files/(?P<name>.*)$', FileView.as_view(),
            name='serve-file'),  # 获取静态文件
    re_path(r'^api/files/(?P<name>.*)$', FileView.as_view(),
            name='serve-file'),  # 获取静态文件
]
