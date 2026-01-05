from django.urls import path

from apps.users.views import login_view, logout_view, register, user_list

urlpatterns = [
    path("", user_list, name="user_list"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/<int:user_id>", logout_view, name="logout"),
]
