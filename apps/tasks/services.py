import logging

from django.db import transaction
from common.permissions import require
from .models.task import Task
from .models.assignment import Assignment
from .models.status_history import StatusHistory

logger = logging.getLogger(__name__)

class TaskService:

    @staticmethod
    @transaction.atomic
    def create_task(*, user, project, data):
        require(
            user.is_admin
            or project.owner == user
            or project.members.filter(id=user.id).exists(),
            "You do not have permission to create tasks in this project"
        )

        task = Task.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            project=project,
            status=data.get("status", Task.status.field.default),
            priority=data.get("priority", Task.priority.field.default),
            due_date=data.get("due_date"),
            created_by=user,
            updated_by=user,
        )

        # Optional assignment
        assignee_id = data.get("assigned_to")
        if assignee_id:
            Assignment.objects.create(
                task=task,
                user_id=assignee_id,
                created_by=user,
            )
        logger.info(
            "task_created",
            extra={
                "taskt_id": task.id,
                "project_id": project.id,
                "user_id": user.id,
            }
        )

        return task

    @staticmethod
    @transaction.atomic
    def update_task(*, task, user, data): 
        require(
            user.is_admin
            or task.project.owner == user
            or task.assignments.filter(user=user).exists(),
            "You do not have permission to update this task"
        )

        old_status = task.status

        for field in ["title", "description", "status", "priority", "due_date"]:
            if field in data:
                setattr(task, field, data[field])

        task.updated_by = user
        task.save()

        # Track status change
        if "status" in data and old_status != task.status:
            StatusHistory.objects.create(
                task=task,
                old_status=old_status,
                new_status=task.status,
                created_by=user,
            )
        logger.info(
            "task_updated",
            extra={
                "taskt_id": task.id,
                "project_id": task.project.id,
                "user_id": user.id,
            }
        )

        return task

    @staticmethod
    @transaction.atomic
    def assign_task(*, task: Task, user, assignee) -> Task:
        """
        Assign a task to a project member.

        Rules:
        - user must be a project member
        - assignee must be a project member
        """

        require(
            user.is_admin or  task.project.owner == user
            or task.assignments.filter(user=user).exists(),
            "You do not have permission to update this task"
        )   

        Assignment.objects.create(
                task=task,
                user=assignee,
                created_by=user,
            )

        return task



