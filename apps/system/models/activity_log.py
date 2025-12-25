from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ("PROJECT_CREATED", "Project created"),
        ("PROJECT_UPDATED", "Project updated"),
        ("PROJECT_DELETED", "Project deleted"),
        ("TASK_CREATED", "Task created"),
        ("TASK_UPDATED", "Task updated"),
        ("TASK_DELETED", "Task deleted"),
        ("TASK_STATUS_CHANGED", "Task status changed"),
        ("TASK_ASSIGNED", "Task assigned"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    # Generic relation → Project / Task / others later
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} by {self.user}"
