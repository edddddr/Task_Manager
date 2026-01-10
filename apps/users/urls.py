from django.urls import path

from apps.users.views import LoginView, LogoutView, RegisterView
# , login_view, logout_view, register, user_list

# urlpatterns = [
#     path("", user_list, name="user_list"),
#     path("register/", register, name="register"),
#     path("login/", login_view, name="login"),
#     path("logout/<int:user_id>", logout_view, name="logout"),
# ]
urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]