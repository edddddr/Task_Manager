import pytest
from rest_framework.test import APIRequestFactory

from apps.projects.models.membership import ProjectRole
from apps.projects.permissions.project import IsProjectAdmin
from apps.projects.tests.factories import MembershipFactory


@pytest.mark.django_db()
def test_is_project_admin_allows_admin():
    membership = MembershipFactory(role=ProjectRole.ADMIN)
    request = APIRequestFactory().delete("/projects/2/")
    request.user = membership.user

    permission = IsProjectAdmin()
    assert permission.has_object_permission(request, None, membership.project)


# from apps.users.tests.factories import UserFactory

# @pytest.mark.django_db()
# def test_user_factory():
#     admin = UserFactory()
#     print(admin.username)

# test_user_factory()
