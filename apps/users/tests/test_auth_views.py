import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.tests.factories import UserFactory



@pytest.mark.django_db
def test_register_view():
    client = APIClient()
    response = client.post(
        reverse("register", kwargs={"version": "v1"}),
        {
            "username": "newuser",
            "email": "new@test.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
        },
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_login_view_returns_tokens():
    user = UserFactory()

    client = APIClient()
    response = client.post(
        reverse("login", kwargs={"version": "v1"}),
        {
            "username": user.username,
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_logout_blacklists_refresh_token():
    user = UserFactory()

    client = APIClient()
    login = client.post(
        reverse("login", kwargs={"version": "v1"}),
        {"username": user.username, "password": "password123"},
    )

    refresh = login.data["refresh"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

    response = client.post(
        reverse("logout", kwargs={"version": "v1"}),
        {"refresh": refresh},
    )

    assert response.status_code == 205
