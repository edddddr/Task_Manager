from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.projects.views import ProjectViewSet
router = DefaultRouter()
# from apps.projects.views import (project_activity, project_detail,
#                                  project_list_create)

# urlpatterns = [
#     path("", project_list_create, name="index"),
#     path("<int:project_id>/", project_detail, name="index"),
#     path("<int:project_id>/tasks/", include("apps.tasks.urls")),
#     path("<int:project_id>/activity/", project_activity, name="project-activity"),
# ]
router.register("projects", ProjectViewSet, basename="project")


urlpatterns = router.urls