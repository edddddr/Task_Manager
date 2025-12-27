from apps.projects.models.project import Project
from apps.projects.tests.factories import ProjectFactory
from apps.users.tests.factories import UserFactory


def test_user_sees_only_member_projects():
    user = UserFactory()
    other = UserFactory()

    project = ProjectFactory(members=[user])
    ProjectFactory(members=[other])

    projects = Project.objects.for_user(user)
    print(user)
    print(projects)

    assert project in projects
    assert projects.count() == 1
# 