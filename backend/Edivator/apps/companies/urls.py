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

from apps.companies.views import CompaniesViewSet

urlpatterns = [
    # 创建企业
    path('create/', CompaniesViewSet.as_view({'post': 'create'})),
    # 添加管理员
    path('appoint_admin/', CompaniesViewSet.as_view({'post': 'appoint_administrator'})),
    # 查询企业创建者
    path('query_admin/<int:pk>/', CompaniesViewSet.as_view({'get': 'get_admin'})),
    # 查询企业的管理员
    path('query_administrators/<int:pk>/', CompaniesViewSet.as_view({'get': 'get_administrators'})),
    # 获取企业的所有团队
    path('query_teams/<int:pk>/', CompaniesViewSet.as_view({'get': 'get_teams'})),
    # 获取企业中的用户
    path('query_users/<int:pk>/', CompaniesViewSet.as_view({'get': 'get_users'})),
    # 获取企业信息
    path('query_detail/<int:pk>/', CompaniesViewSet.as_view({'get': 'get_detail'})),
    # 删除企业
    path('delete/<int:pk>/', CompaniesViewSet.as_view({'delete': 'destroy'})),


    path('query_teams_short/<int:pk>/', CompaniesViewSet.as_view({'get': 'get_teams_short'})),
]
