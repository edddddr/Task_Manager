from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.projects.views import ProjectViewSet
router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")


urlpatterns = router.urls