from rest_framework import permissions
from rest_framework.views import View, Request

from users.models import User
from reviews.models import Review


class IsAdmin(permissions.BasePermission):
    def has_permission(self, req: Request, view: View) -> bool:
        return bool(req.user.is_authenticated and req.user.is_superuser)


class IsAdminOrReadyOnly(permissions.BasePermission):
    def has_permission(self, req: Request, view: View) -> bool:
        return bool(
            req.method in permissions.SAFE_METHODS
            or req.user.is_authenticated
            and req.user.is_superuser
        )


class IsAdminOrCritic(permissions.BasePermission):
    def has_permission(self, req: Request, view: View) -> bool:
        return bool(
            req.method in permissions.SAFE_METHODS
            or req.user.is_authenticated
            and req.user.is_critic
            or req.user.is_authenticated
            and req.user.is_superuser
        )


class IsCriticAndOwner(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: User) -> bool:
        return bool(
            req.user.is_authenticated and req.user.is_critic and obj == req.user
        )


class IsCriticAndReviewOwner(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: Review) -> bool:
        return bool(
            req.user.is_authenticated and req.user.is_critic and obj.user == req.user
        )
