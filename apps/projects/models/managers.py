from django.db import models
from apps.projects.models.querysets import ProjectQuerySet


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def created_by(self, user):
        return self.get_queryset().created_by(user)

    def with_tasks(self):
        return self.get_queryset().with_tasks()
    

    # Creation logic
    # def create_project_for_user(self, user, name, description=""):
    #     if not (user.is_admin or user.is_manager):
    #         raise PermissionError("You do not have permission to create a project.")
    #     project = self.model.objects.create(
    #         name=name,
    #         description=description,
    #         created_by=user
    #     )
    #     project.members.add(user)
    #     return project

    def visible_to(self, user):
        return self.get_queryset().for_user(user).with_members()
