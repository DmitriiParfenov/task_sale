from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsActiveAndIsOwner(BasePermission):
    """
    Доступ разрешен только активированным пользователям. Детали записей могут смотреть только владельцы записей.
    Пользователь может видеть список всех контактов без возможности их как-то редактировать или удалять, если он не
    является их владельцем.
    """
    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user == obj.product_user
        elif request.method in ('PATCH', 'PUT', 'POST'):
            return request.user == obj.product_user
        elif request.method == 'DELETE':
            if not request.user.is_active:
                return False
            return request.user == obj.product_user or request.user.is_superuser
        return False
