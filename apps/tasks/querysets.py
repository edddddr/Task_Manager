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
        Tasks assigned to a user.
        Uses M2M JOIN efficiently.
        """
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
