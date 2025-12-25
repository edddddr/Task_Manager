
from django.core.exceptions import PermissionDenied


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


def is_manager(user):
    return user.is_authenticated and user.role == "manager"


def is_member(user):
    return user.is_authenticated and user.role == "member"


def can_edit_project(user, project):
    if is_admin(user):
        return True
    if is_manager(user) and project.created_by == user:
        return True
    return 




def can_edit_task(user, task):
    if is_admin(user):
        return True
    if task.assigned_to == user:
        return True
    return False


def can_delete_task(user, task):
    if is_admin(user):
        return True
    if is_manager(user):
        return True
    return False


def require(condition: bool, message="Permission denied"):
    if not condition:
        raise PermissionDenied(message)
