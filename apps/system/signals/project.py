from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from apps.projects.models.project import Project
from apps.system.models.activity_log import ActivityLog


@receiver(post_save, sender=Project)
def log_project_save(sender, instance, created, **kwargs):
    ActivityLog.objects.create(
        user=instance.updated_by or instance.created_by,
        action="PROJECT_CREATED" if created else "PROJECT_UPDATED",
        content_type=ContentType.objects.get_for_model(Project),
        object_id=instance.id,
        metadata={
            "name": instance.name,
        },
    )


@receiver(pre_delete, sender=Project)
def log_project_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        user=instance.updated_by,
        action="PROJECT_DELETED",
        content_type=ContentType.objects.get_for_model(Project),
        object_id=instance.id,
        metadata={
            "name": instance.name,
        },
    )
