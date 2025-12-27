import factory
from apps.tasks.models.task import Task
from apps.projects.tests.factories import ProjectFactory
from apps.users.tests.factories import UserFactory


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text")

    project = factory.SubFactory(ProjectFactory)
    created_by = factory.SelfAttribute("project.owner")

    status = "todo"
