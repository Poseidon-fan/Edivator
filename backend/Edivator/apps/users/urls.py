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
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.users import views
from apps.users.views import LoginView, RegisterView

urlpatterns = [
    # 登录
    path('login/', LoginView.as_view(), name='login'),
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    # 刷新token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 校验token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 获取单个用户信息
    path('<int:pk>/', views.UserView.as_view({'get': 'retrieve'}), name='user_detail'),
    # 上传图片
    path('<int:pk>/avatar/upload/', views.UserView.as_view({'post': 'upload_avatar'}), name='upload_avatar'),
    # 通过邀请码加入企业
    path('join_company/', views.UserView.as_view({'post': 'join_company'}), name='join_company'),
    # 获取用户信息
    path('me/', views.UserView.as_view({'get': 'get_detail'}), name='me'),
    # 获取文档总数
    path('get_doc_num/', views.UserView.as_view({'get': 'get_doc_nums'})),
    # 充值
    path('recharge/', views.UserView.as_view({'post': 'recharge'})),
]
