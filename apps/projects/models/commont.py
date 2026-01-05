from django.db import models

from apps.system.models.base_models import AuditModel, SoftDeleteModel


class Comment(SoftDeleteModel, AuditModel):
    task = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField()

    def __str__(self):
        return f"Comment on {self.task_id}"
