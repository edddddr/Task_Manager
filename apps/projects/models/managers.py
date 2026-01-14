from django.db import models

from apps.projects.models.querysets import ProjectQuerySet


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db).active()

    # def get_queryset(self):
    #     return SoftDeleteQuerySet(self.model, using=self._db).active()

    def active(self):
        return self.get_queryset().active()

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def created_by(self, user):
        return self.get_queryset().created_by(user)

    def with_tasks(self):
        return self.get_queryset().with_tasks()

    def visible_to(self, user):
        return self.get_queryset().for_user(user).with_members()
