from django.urls import path

from apps.tasks.views import task_activity, task_detail, task_list_create

urlpatterns = [
    path("", task_list_create, name="task-list-create"),
    path("<int:task_id>/", task_detail, name="task-detail"),
    path("<int:task_id>/activity/", task_activity, name="task-activity"),
]
