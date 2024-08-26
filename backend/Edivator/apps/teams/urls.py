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
from .views import TeamViewSet, MessageViewSet, NotificationViewSet

urlpatterns = [
    # 创建团队
    path('create/', TeamViewSet.as_view({'post': 'create'})),
    # 拉人进团队
    path('add_user/', TeamViewSet.as_view({'post': 'add_user'})),
    # 查询团队用户
    path('query_users/<int:pk>/', TeamViewSet.as_view({'get': 'get_users'})),
    # 查询团队信息
    path('query_detail/<int:pk>/', TeamViewSet.as_view({'get': 'get_detail'})),
    # 查询某个用户所在的企业里所在的所有团队
    path('query_belonged_teams/', TeamViewSet.as_view({'get': 'get_user_company_teams'})),
    # 退出团队
    path('exit/<int:pk>/', TeamViewSet.as_view({'post': 'exit'})),

    # 申请加入团队
    path('messages/applicate/', MessageViewSet.as_view({'post': 'create'})),
    # 批准进入团队
    path('messages/approve/<int:pk>/', MessageViewSet.as_view({'post': 'approve'})),
    # 拒绝进入团队
    path('messages/reject/<int:pk>/', MessageViewSet.as_view({'post': 'reject'})),
    # 获取自己所有的请求列表
    path('messages/query_mine/', MessageViewSet.as_view({'get': 'my_requests'})),
    # 获取当前企业里处理pending状态的消息
    path('messages/query_pendings/', MessageViewSet.as_view({'get': 'pending_requests'})),
    # 获取通知
    path('notifications/', NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
    # 标记通知为已读
    path('notifications/mark-as-read/', NotificationViewSet.as_view({'post': 'mark_as_read'}), name='notification-mark-as-read'),

    # 删除团队
    path('delete/<int:pk>/', TeamViewSet.as_view({'delete': 'destroy'}))
]
