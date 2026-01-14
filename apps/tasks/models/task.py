from django.conf import settings  # Reusable app for user
from django.db import models

from apps.system.models.activity_log import ActivityLog
from apps.system.models.base_models import AuditModel, SoftDeleteModel
from apps.tasks.models.manager import TaskManager
from apps.users.models import User


class TaskStatus(models.TextChoices):
    TODO = "todo", "To Do"
    IN_PROGRESS = "in_progress", "In Progress"
    DONE = "done", "Done"


class TaskPriority(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"


class Task(SoftDeleteModel, AuditModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="tasks"
    )  # 'projects.Project' This uses lazy loading and avoids circular imports

    status = models.CharField(max_length=20, choices=TaskStatus.choices, default="todo")
    priority = models.CharField(
        max_length=20, choices=TaskPriority.choices, default="medium"
    )
    
    due_date = models.DateTimeField(null=True, blank=True)

    objects = TaskManager()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "project": self.project.id,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            # 🔹 BTREE indexes (default)
            models.Index(fields=["status"]),
            models.Index(fields=["project"]),
        ]

    def __str__(self):
        return self.title
