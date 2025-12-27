import factory
from apps.projects.models.project import Project
from apps.users.tests.factories import UserFactory

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
    owner = factory.SubFactory(UserFactory)
    created_by = factory.SelfAttribute("owner")
    updated_by = factory.SelfAttribute("owner")

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        # Add the members passed in: ProjectFactory(members=[user])
        for member in extracted:
            self.members.add(member)
            print("member is created")