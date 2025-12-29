import logging

from django.db import transaction
from django.core.exceptions import PermissionDenied
from .models.project import Project
from common.permissions import require

logger = logging.getLogger(__name__)

class ProjectService:

    @staticmethod
    @transaction.atomic
    def create_project(*, user, data):
        require(user.is_authenticated, "Authentication required")


        project = Project.objects.create(
            name=data["name"],
            description=data.get("description", ""),
            owner=user,
            created_by=user,
            updated_by=user,
        )

        # Owner is always a member
        project.members.add(user)
        logger.info(
            "project_created",
            extra={
                "project_id": project.id,
                "user_id": user.id,
            }
        )

        return project

    @staticmethod
    @transaction.atomic
    def update_project(*, project, user, data):
        require(
            user.is_admin or project.owner == user,
            "You do not have permission to update this project"
        )
        print("yes authenticated")


        for field in ["name", "description"]:
            if field in data:
                setattr(project, field, data[field])

        project.updated_by = user
        project.save()
        logger.info(
            "project_updated",
            extra={
                "project_id": project.id,
                "user_id": user.id,
            }
        )

        return project
