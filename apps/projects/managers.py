from django.db import models
from apps.projects.querysets import ProjectQuerySet


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def visible_to(self, user):
        return self.get_queryset().for_user(user).with_members()
