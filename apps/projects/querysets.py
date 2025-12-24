from django.db import models
from django.db.models import Q


class ProjectQuerySet(models.QuerySet):
    """
    In Django, models.QuerySet is a collection 
    of objects from your database. It is the primary 
    tool used to read, filter, and order data through 
    Django's Object-Relational Mapping (ORM).
    """


    def active(self):
        return self.filter(is_active=True)

    def created_by(self, user):
        return self.filter(created_by=user)

    def with_tasks(self):
        return self.prefetch_related("tasks")
    
    def for_user(self, user):
        """
        Return projects visible to a user.
        Logical optimization: filter early.
        """
        return self.filter(
            Q(created_by=user) |
            Q(members=user)
        ).distinct()

    def with_members(self):
        """
        Avoid N+1 queries when accessing members.
        """
        return self.prefetch_related("members")

    def recent(self):
        """
        Common access pattern.
        """
        return self.order_by("-created_at")
