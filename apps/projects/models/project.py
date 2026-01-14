from django.conf import settings
from django.db import models

from apps.projects.models.managers import \
    ProjectManager  # Reusable app for user
from apps.system.models.base_models import AuditModel, SoftDeleteModel


class Project(SoftDeleteModel, AuditModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_projects",
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="projects.ProjectMembership",
        related_name="projects",
    )

    objects = ProjectManager()

    def update_project(self, *, name=None, description=None):
        """
        Update allowed fields only.
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.save()
        return self

    def to_dict(self):
        """
        Serialize project to JSON-safe dict.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by.id if self.created_by else None,
            "members": list(self.members.values_list("id", flat=True)),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    class Meta:
        indexes = [
            models.Index(fields=["created_by"]),
            models.Index(fields=["created_at"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner"],
                name="unique_project_name_per_owner",
            )
        ]

    def __str__(self):
        return self.name
