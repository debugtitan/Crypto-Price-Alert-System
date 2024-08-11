import pytest
from rest_framework.test import APIClient
from core.v1.users.models import User
from core.utils.helpers import security, redis
from unittest.mock import patch, MagicMock


@pytest.fixture
def user(db):
    return User.objects.create(email="test@debug.com", is_email_verified=True)


@pytest.fixture
def token():
    return security.Token.create_otp()


@pytest.mark.django_db
def test_initialize_email_login(user, token):
    client = APIClient()
    with patch.object(
        redis.RedisTools, "cache_value", new_callable=MagicMock
    ) as mock_cache:
        response = client.post(
            "/api/v1/auth/initialize_email_login", {"email": user.email}
        )
        assert response.status_code == 200
        assert "A login code has been sent to" in response.data["message"]


@pytest.mark.django_db
@patch("core.utils.tasks.send_email_to_address.apply_async")
def test_initialize_email_login_for_unregistered_email(mock_send_email, token):
    client = APIClient()
    unregistered_email = "titan@debug.com"

    response = client.post(
        "/api/v1/auth/initialize_email_login", {"email": unregistered_email}
    )
    assert response.status_code == 200
    assert "A login code has been sent to" in response.data["message"]


@pytest.mark.django_db
@patch("core.utils.helpers.redis.RedisTools")
def test_finalize_email_login_with_valid_data(mock_redis, user):
    client = APIClient()
    token = security.Token.create_otp()
    mock_redis.return_value = MagicMock(cache_value={"email": user.email})

    response = client.post(
        "/api/v1/auth/finalize_email_login", {"token": token, "email": user.email}
    )
    assert response.status_code == 200
    assert "token" in response.data
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_finalize_email_login_with_invalid_token(user):
    client = APIClient()
    invalid_token = "invalid_token"
    email = user.email

    response = client.post(
        "/api/v1/auth/finalize_email_login", {"token": invalid_token, "email": email}
    )
    assert response.status_code == 400
    assert response.data["message"] == "You specified an invalid token"


@pytest.mark.django_db
def test_finalize_email_login_with_invalid_email(user):
    client = APIClient()
    token = security.Token.create_otp()
    valid_token = token
    invalid_email = "invalid_email@debug.com"

    # Patching RedisTools to simulate invalid email case
    with patch.object(
        redis.RedisTools, "cache_value", new_callable=MagicMock
    ) as mock_cache:
        mock_cache.return_value = {"email": "team_email@debug.com"}

        response = client.post(
            "/api/v1/auth/finalize_email_login",
            {"token": valid_token, "email": invalid_email},
        )
        assert response.status_code == 400
        assert response.data["message"] == "You specified an invalid email"
