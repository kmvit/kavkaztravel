import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from custom_notifications.models import NotificationSettings

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser", password="testpass123", email="test@example.com"
    )


@pytest.fixture
def user1(db):
    return User.objects.create_user(
        username="testuser1", password="test1pass123", email="test1@example.com"
    )


@pytest.fixture
def test_settings(db, user):
    return NotificationSettings.objects.create(user=user, email=True)


@pytest.fixture
def auth_client(api_client, user):
    client = api_client
    client.force_authenticate(user=user)
    return client
