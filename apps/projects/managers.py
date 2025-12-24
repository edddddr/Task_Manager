from django.db import models
from apps.projects.querysets import ProjectQuerySet


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()

    def created_by(self, user):
        return self.get_queryset().created_by(user)

    def with_tasks(self):
        return self.get_queryset().with_tasks()

    # Creation logic
    def create_project(self, name, description, creator):
        return self.create(
            name=name,
            description=description,
            created_by=creator
        )

    def visible_to(self, user):
        return self.get_queryset().for_user(user).with_members()
