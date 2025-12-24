from django.db import models
from .querysets import TaskQuerySet


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def for_project(self, project):
        return self.get_queryset().for_project(project)

    def create_task(self, project, data):
        return self.create(
            title=data.get("title"),
            description=data.get("description", ""),
            status=data.get("status", "todo"),
            priority=data.get("priority", "medium"),
            project=project,
            assigned_to_id=data.get("assigned_to")
        )

    def dashboard_tasks(self, user):
        """
        High-level business query.
        """
        return (
            self.get_queryset()
            .for_user(user)
            .with_related()
            .due_soon()
        )
