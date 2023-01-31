from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    message = "You must be the creator of this restaurant."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.created_by == request.user) or request.user.is_superuser
