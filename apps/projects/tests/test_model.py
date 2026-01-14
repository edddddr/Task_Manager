import pytest
from apps.projects.models.project import Project


@pytest.mark.django_db
def test_update_project():
    project = Project.objects.create(name="Old", description="Old desc")
    project.update_project(name="New")

    assert project.name == "New"
