import pytest
from apps.projects.services import ProjectService
from apps.system.models.activity_log import ActivityLog
from apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db
# @pytest.mark.django_db

def test_activity_log_created_on_project_creation():
    user = UserFactory()

    ProjectService.create_project(
        user=user,
        data={"name": "Tracked"},
    )

    log = ActivityLog.objects.first()

    assert log.actor == user
    assert log.action == "PROJECT_CREATED"


# from django.db import IntegrityErro
# def test_activity_log_cannot_be_created_manually():
#     with pytest.raises(IntegrityError):
#         ActivityLog.objects.create(action="hack")
