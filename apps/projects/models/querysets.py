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
        Return projects visible to the given user.
        - Admin sees all
        - Manager sees all projects they created or are member of
        - Member sees only projects they are a member of
        """
        if user.is_admin:
            return self.active()
        elif user.is_manager:
            return self.active().filter(
                models.Q(created_by=user) | models.Q(members=user)
            )
        else:  # member
            return self.active().filter(members=user)

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
