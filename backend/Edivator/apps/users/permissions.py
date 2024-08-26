from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from apps.users.models import User


class UserPermission(permissions.BasePermission):
    """用户权限"""
    def has_object_permission(self, request, view, obj):
        # 判断是否为管理员账号
        if request.user.is_superuser:
            return True
        # 如果不是管理员，判断操作对象和登录对象是否为同一个
        return obj == request.user


class SuperUserPermission(permissions.BasePermission):
    """超级管理员权限"""
    def has_permission(self, request, view):
        # 检查用户是否是管理员（超级用户）
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


# class AdminPermission(permissions.BasePermission):
#     """企业管理员权限"""
#     def has_permission(self, request, view):
#         admin_id = request.data.get('admin')
#         if admin_id is None:
#             raise PermissionDenied("admin参数不可省略")
#
#         if not isinstance(admin_id, int):
#             admin_id = int(admin_id)
#
#         # 检查admin_id是否等于当前登录用户的ID
#         if admin_id != request.user.id:
#             raise PermissionDenied("身份校验未通过")
#
#         return True
