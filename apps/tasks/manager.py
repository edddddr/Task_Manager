from django.db import models
from .querysets import TaskQuerySet
from apps.users.models import User


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def for_project(self, project):
        return self.get_queryset().for_project(project)
    
    def for_user(self, user):
        return self.get_queryset().for_user(user)
        
    def create_task(self, project, data):
        return self.create(
            title=data.get("title"),
            description=data.get("description", ""),
            status=data.get("status", "todo"),
            priority=data.get("priority", "medium"),
            project=project,
            assigned_to_id=data.get("assigned_to")
        )
    
    def create_task_for_user(self, user, project, data):
        if not (user.is_admin or user.is_manager):
            raise PermissionError("Not allowed")
        return self.create_task(project=project, data=data)
    

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
