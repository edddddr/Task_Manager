from django.urls import path
from apps.tasks.views import task_list_create, task_detail

urlpatterns = [
    path("", task_list_create, name="task-list-create"),
    path("<int:task_id>/", task_detail, name="task-detail"),
]
