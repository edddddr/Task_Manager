import json
import pytest
from apps.tasks.models.task import Task
from apps.projects.tests.factories import ProjectFactory
from apps.tasks.tests.refactories import TaskFactory
from apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db

BASE_URL = '/api/v1/projects'

def test_create_task_success(client):
    project = ProjectFactory()
    user = project.owner
    # print(" -- -- - -", user)

    client.force_login(user)

    payload = {"title": "HTTP Task"}

    response = client.post(
        f"{BASE_URL}/{project.id}/tasks/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 201
    assert Task.objects.count() == 1


def test_create_task_forbidden_for_non_member(client):
    project = ProjectFactory()
    outsider = UserFactory()
    client.force_login(outsider)

    response = client.post(
        f"/projects/{project.id}/tasks/",
        data=json.dumps({"title": "Hack"}),
        content_type="application/json",
    )

    assert response.status_code == 403
    assert Task.objects.count() == 0


def test_delete_task_soft_deletes(client):
    project = ProjectFactory()
    user = project.owner
    task = TaskFactory(project=project)

    client.force_login(user)

    response = client.delete(f"/tasks/{task.id}/")

    assert response.status_code == 200

    task.refresh_from_db()
    assert task.is_active is False
