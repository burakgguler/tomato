from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    message = "You must be the creator of this comment."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user) or request.user.is_superuser
