from django.contrib import admin
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'date_joined')

admin.site.register(Task)
admin.site.register(Project)

