from rest_framework import permissions
from review.models import Review


class ReviewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_superuser or request.user.is_critic


class ReviewDetailPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Review):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_critic and obj.critic == request.user
