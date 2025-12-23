from django.db import models
from django.db.models import Q


class ProjectQuerySet(models.QuerySet):

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
