from django.conf import settings
from django.db import models

from apps.system.models.base_models import AuditModel


class Assignment(AuditModel):
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_by",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "user"],
                name="unique_task_assignment",
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.task}"
