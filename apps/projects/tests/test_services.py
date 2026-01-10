import pytest

from apps.projects.services import ProjectService
from apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_project_creator_is_added_as_member():
    user = UserFactory()

    project = ProjectService.create_project(
        user=user,
        data={"name": "Alpha"},
    )

    assert user in project.members.all()


def test_project_creator_fields_are_set():
    user = UserFactory()

    project = ProjectService.create_project(
        user=user,
        data={"name": "Alpha"},
    )

    assert project.owner == user
    assert project.created_by == user
    assert project.updated_by == user
