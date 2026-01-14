import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.projects.tests.factories import UserFactory, ProjectFactory, MembershipFactory
from apps.projects.models.membership import ProjectRole


@pytest.mark.django_db
def test_project_list_only_user_projects():
    user = UserFactory()
    project = ProjectFactory()
    MembershipFactory(user=user, project=project)

    client = APIClient()
    client.force_authenticate(user)

    response = client.get(reverse("project-list", kwargs={"version": "v1"}))

    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_can_create_task():
    user = UserFactory()
    project = ProjectFactory(owner=user)
    MembershipFactory(user=user, project=project, role=ProjectRole.ADMIN)

    client = APIClient()
    client.force_authenticate(user)

    response = client.post(
        reverse("project-tasks", kwargs={
        "version": "v1", 
        "pk": project.id
    }),
        {"title": "Task 1", 
        "description": "Task description", 
        "project": project.id
        },
    )

    assert response.status_code == 201
