import factory
from django.contrib.auth import get_user_model

from apps.projects.models.membership import ProjectMembership, ProjectRole
from apps.projects.models.project import Project
from apps.tasks.models.task import Task

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ()

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")

    password = factory.PostGenerationMethodCall("set_password", "password123")



class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"Project {n}")
    owner = factory.SubFactory(UserFactory)


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectMembership

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    role = ProjectRole.VIEWER


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = "Test Task"
    project = factory.SubFactory(ProjectFactory)
