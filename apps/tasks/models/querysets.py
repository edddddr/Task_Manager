from django.db import models


class TaskQuerySet(models.QuerySet):

    def for_project(self, project):
        return self.filter(project=project)

    def assigned(self):
        return self.filter(assigned_to__isnull=False)
    
    def with_assignee(self):
        return self.prefetch_related("assigned_to")

    def for_user(self, user):
        """
        Return tasks visible to the user.
        - Admin sees all
        - Manager sees tasks in projects they created or are member of
        - Member sees only tasks assigned to them
        """
        if user.is_admin:
            return self
        elif user.is_manager:
            return self.filter(
                models.Q(project__created_by=user) | models.Q(project__members=user)
            )
        else:  # member
            return self.filter(assigned_to=user)

    def by_status(self, status):
        return self.filter(status=status)

    def with_related(self):
        """
        Physical + logical optimization together.
        """
        return self.select_related("project").prefetch_related("assigned_to")

    def due_soon(self):
        return self.filter(due_date__isnull=False).order_by("due_date")
