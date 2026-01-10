import pytest
from django.core.exceptions import PermissionDenied

from apps.projects.tests.factories import ProjectFactory
from apps.tasks.services import TaskService
from apps.tasks.tests.refactories import TaskFactory
from apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db
# @pytest.mark.django_db


def test_task_is_created_for_project():
    project = ProjectFactory()
    user = project.owner

    task = TaskService.create_task(
        user=user,
        project=project,
        data={"title": "Test task"},
    )

    assert task.project == project
    assert task.created_by == user


def test_task_can_only_be_assigned_to_project_member():
    project = ProjectFactory()
    outsider = UserFactory()

    with pytest.raises(PermissionDenied):
        TaskService.assign_task(
            task=TaskFactory(project=project),
            user=project.owner,
            assignee=outsider,
        )
