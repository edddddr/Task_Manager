from django.conf import settings
from django.contrib import admin
from django.urls import include, path


from apps.users.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/<str:version>/", include("apps.users.urls")),
    path("api/<str:version>/", include("apps.projects.urls")),
]




if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
