from django.urls import path, include
from apps.projects.views import project_list_create, project_detail, project_activity

urlpatterns = [
    path('', project_list_create, name='index'),
    path('<int:project_id>/', project_detail, name='index'),
    path('<int:project_id>/tasks/', include('apps.tasks.urls')),
    path('<int:project_id>/activity/', project_activity, name='project-activity'),
   
]
