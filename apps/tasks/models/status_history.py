from django.db import models

from apps.system.models.base_models import AuditModel


class StatusHistory(AuditModel):
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="status_history",
    )

    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.old_status} → {self.new_status}"
