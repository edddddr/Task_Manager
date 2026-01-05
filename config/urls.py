from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),

    # path("api/token/", TokenObtainPairView.as_view()),
    # path("api/token/refresh/", TokenRefreshView.as_view()),

    path(
        "api/<str:version>/auth/login/", 
        TokenObtainPairView.as_view(), 
        name="login"
        ),  
    path(
        "api/<str:version>/auth/refresh/", 
        TokenRefreshView.as_view(), 
        name="refresh"
        ),
    path(
        "api/<str:version>/auth/logout/",
        LogoutView.as_view(), 
        name="logout"
        ),
        
    path("api/<str:version>/", include("apps.users.urls")),
    # path("api/<str:version>/", include("projects.urls")),
]
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/v1/users/", include("apps.users.urls")),
#     path("api/v1/tasks/", include("apps.tasks.urls")),
#     path("api/v1/projects/", include("apps.projects.urls")),
# ]




if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
