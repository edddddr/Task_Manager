from django.db import models
from .querysets import TaskQuerySet


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def for_project(self, project):
        return self.get_queryset().for_project(project)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def dashboard_tasks(self, user):
        """
        High-level business query.
        """
        return self.get_queryset().for_user(user).with_related().due_soon()
