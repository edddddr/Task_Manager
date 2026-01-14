import pytest
from apps.tasks.models.task import Task, TaskStatus
from tests.factories import ProjectFactory


@pytest.mark.django_db
def test_task_defaults():
    project = ProjectFactory()
    task = Task.objects.create(title="Task", project=project)

    assert task.status == TaskStatus.TODO
