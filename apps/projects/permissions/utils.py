from apps.projects.models import ProjectMembership


def get_user_role(user, project):
    try:
        membership = ProjectMembership.objects.get(
            user=user,
            project=project,
        )
        return membership.role
    except ProjectMembership.DoesNotExist:
        return None
