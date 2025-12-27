from apps.projects.models.project import Project
from apps.projects.tests.factories import ProjectFactory


def test_project_soft_delete_sets_flag():
    project = ProjectFactory()

    project.delete()

    project.refresh_from_db()
    assert project.is_active is False
    assert project.deleted_at is not None


def test_soft_deleted_projects_are_hidden():
    ProjectFactory()
    deleted = ProjectFactory()
    deleted.delete()


    assert Project.objects.count() == 1