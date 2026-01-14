import pytest
from apps.users.serializers import RegisterSerializer


@pytest.mark.django_db
def test_register_serializer_creates_user():
    serializer = RegisterSerializer(
        data={
            "username": "alice",
            "email": "alice@test.com",
            "password": "password123",
            "first_name": "Alice",
            "last_name": "Doe",
        }
    )

    assert serializer.is_valid()
    user = serializer.save()

    assert user.username == "alice"
    assert user.check_password("password123")
