import pytest

from apps.users.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        username="john",
        email="john@test.com",
        password="password123",
    )

    assert user.username == "john"
    assert user.check_password("password123")
    assert user.is_active is True
