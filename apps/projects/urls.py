from django.urls import path
from apps.projects.views import project_list_create, project_detail

urlpatterns = [
    path('', project_list_create, name='index'),
    path('<int:project_id>/', project_detail, name='index'),
]
