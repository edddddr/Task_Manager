from django.urls import path
from apps.users.views import user_list, register, login_view, logout_view

urlpatterns = [
    path('', user_list, name='user_list'),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/<int:user_id>", logout_view, name="logout"),
]
