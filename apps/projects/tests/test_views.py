import json
import pytest
from django.urls import reverse
from apps.projects.tests.factories import ProjectFactory
from apps.users.models import User
from apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db
BASE_URL = "/api/v1/projects/"

def test_get_projects_returns_only_user_projects(client):
    user = UserFactory()
    other = UserFactory()

    visible = ProjectFactory()
    visible.members.add(user)

    hidden = ProjectFactory()
    hidden.members.add(other)

    client.force_login(user)

    response = client.get(BASE_URL)
    print(" --- -- -- - ", response.status_code)

    assert response.status_code == 200
    data = response.json()
    print(" --- -- -- -", data)

    project_ids = [p["id"] for p in data]
    assert visible.id in project_ids
    assert hidden.id not in project_ids



def test_create_project_success(client):
    user = UserFactory()
    client.force_login(user)

    payload = {
        "name": "Integration Project",
        "description": "Created via HTTP",
    }

    response = client.post(
        BASE_URL,
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 201

    data = response.json()["project"]
    assert data["name"] == "Integration Project"


def test_delete_project_forbidden_for_non_admin(client):
    """
    Docstring for test_delete_project_forbidden_for_non_admin
    
    :param client: Description
    :type client: Any
    :In the case of the func Project.objects.for_user(request.user) is early if the user have access the data or not.

    """
    admin = UserFactory(role=User.ROLE_ADMIN)
    member = UserFactory(role=User.ROLE_MEMBER)
    
    # more professional 
    # admin = UserFactory(admin=True)
    # member = UserFactory()
    project = ProjectFactory(owner=admin)
    client.force_login(member)

    response = client.delete(f"{BASE_URL}{project.id}/")

    assert response.status_code == 403
