from django.db import models
from apps.users.models import User



class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    members = models.ManyToManyField(User, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    @classmethod
    def create_project(cls, *, name, description, creator):
        """
        Factory method for creating a project.
        """
        project = cls.objects.create(
            name=name,
            description=description,
            created_by=creator
        )
        project.members.add(creator)
        return project



    def update_project(self, *, name=None, description=None):
        """
        Update allowed fields only.
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.save()
        return self



    def to_dict(self):
        """
        Serialize project to JSON-safe dict.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by.id if self.created_by else None,
            "members": list(self.members.values_list("id", flat=True)),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

