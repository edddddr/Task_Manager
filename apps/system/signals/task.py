from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from apps.tasks.models.task import Task
from apps.system.models.activity_log import ActivityLog


@receiver(post_save, sender=Task)
def log_task_save(sender, instance, created, **kwargs):
    action = "TASK_CREATED" if created else "TASK_UPDATED"

    ActivityLog.objects.create(
        user=instance.updated_by or instance.created_by,
        action=action,
        content_type=ContentType.objects.get_for_model(Task),
        object_id=instance.id,
        metadata={
            "title": instance.title,
            "status": instance.status,
            "priority": instance.priority,
            "project_id": instance.project_id,
        },
    )


@receiver(pre_delete, sender=Task)
def log_task_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        user=instance.updated_by,
        action="TASK_DELETED",
        content_type=ContentType.objects.get_for_model(Task),
        object_id=instance.id,
        metadata={
            "title": instance.title,
        },
    )
