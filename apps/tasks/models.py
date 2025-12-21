from django.db  import models
from django.conf import settings # Reusable app for user



class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    project = models.ForeignKey('projects.Project' , on_delete=models.CASCADE, related_name='tasks')# 'projects.Project' This uses lazy loading and avoids circular imports.
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    @classmethod
    def create_task(cls, *, project, data):
        assigned_to = None
        if data.get("assigned_to"):
            assigned_to = User.objects.get(id=data["assigned_to"])

        return cls.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "todo"),
            priority=data.get("priority", "medium"),
            project=project,
            assigned_to=assigned_to,
            due_date=data.get("due_date")
        )

    def update_task(self, data):
        self.title = data.get("title", self.title)
        self.description = data.get("description", self.description)
        self.status = data.get("status", self.status)
        self.priority = data.get("priority", self.priority)

        if "assigned_to" in data:
            self.assigned_to = (
                User.objects.get(id=data["assigned_to"])
                if data["assigned_to"]
                else None
            )

        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "project": self.project.id,
            "assigned_to": self.assigned_to.id if self.assigned_to else None,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self):
        return self.title
