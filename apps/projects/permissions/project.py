from rest_framework.permissions import BasePermission

from apps.projects.models.membership import ProjectRole
from apps.projects.permissions.utils import get_user_role


class IsProjectAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return get_user_role(request.user, obj) == ProjectRole.ADMIN


class IsProjectEditor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return get_user_role(request.user, obj) in {
            ProjectRole.ADMIN,
            ProjectRole.EDITOR,
        }


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return get_user_role(request.user, obj) is not None
