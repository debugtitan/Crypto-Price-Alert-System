import pytest
from rest_framework.test import APIClient
from core.v1.users.models import User
from core.v1.alerts.models import Alert
from core.utils.enums import DirectionType


@pytest.fixture
def user(db):
    return User.objects.create(email="test@debug.com", is_email_verified=True)


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_list_alerts(authenticated_client, user):
    # Create a sample alert
    Alert.objects.create(owner=user, target_price=500.0)

    response = authenticated_client.get("/api/v1/alerts/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["target_price"] == "500.00"  # decimal points is always 2


@pytest.mark.django_db
def test_create_alert(authenticated_client):
    data = {"target_price": 600.0}

    response = authenticated_client.post("/api/v1/alerts/", data)
    assert response.status_code == 201
    assert response.data["target_price"] == "600.00"
    assert response.data["direction"] == DirectionType.HIGH.value


@pytest.mark.django_db
def test_create_alert_with_direction(authenticated_client):
    data = {"target_price": 600.0, "direction": "LOW"}

    response = authenticated_client.post("/api/v1/alerts/", data)
    assert response.status_code == 201
    assert response.data["target_price"] == "600.00"
    assert response.data["direction"] != DirectionType.HIGH.value
    assert response.data["direction"] == DirectionType.LOW.value


@pytest.mark.django_db
def test_delete_alert(authenticated_client, user):
    alert = Alert.objects.create(owner=user, target_price=50000.0)

    response = authenticated_client.delete(f"/api/v1/alerts/{alert.id}/")
    assert response.status_code == 204
    assert not Alert.objects.filter(id=alert.id).exists()


@pytest.mark.django_db
def test_delete_nonexistent_alert(authenticated_client):
    response = authenticated_client.delete("/api/v1/alerts/999/")
    assert response.status_code == 404
