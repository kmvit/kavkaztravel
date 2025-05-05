"""Тесты API для управления настройками уведомлений."""

from rest_framework import status


BASE_URL = "/api/v1/notificationsnotification-settings"


def test_create_settings_success(auth_client):
    """Тест успешного создания настроек уведомлений."""
    response = auth_client.post(f"{BASE_URL}/", {"email": True})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] is True


def test_create_duplicate_fails(auth_client, test_settings):
    """Тест предотвращения создания дубликата настроек."""
    response = auth_client.post(f"{BASE_URL}/", {"email": False})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "уже существуют" in str(response.data)


def test_get_settings_success(auth_client, test_settings):
    """Тест успешного получения настроек."""
    response = auth_client.get(f"{BASE_URL}/{test_settings.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] is True


def test_list_settings(auth_client, test_settings):
    """Тест получения списка настроек."""
    response = auth_client.get(f"{BASE_URL}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_full_update(auth_client, test_settings):
    """Тест полного обновления настроек."""
    response = auth_client.put(f"{BASE_URL}/{test_settings.id}/", {"email": False})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] is False


def test_partial_update(auth_client, test_settings):
    """Тест частичного обновления настроек."""
    response = auth_client.patch(f"{BASE_URL}/{test_settings.id}/", {"email": False})
    assert response.status_code == status.HTTP_200_OK


def test_delete_settings(auth_client, test_settings):
    """Тест удаления настроек."""
    response = auth_client.delete(f"{BASE_URL}/{test_settings.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_unauthenticated_access(api_client):
    """Тест доступа без аутентификации."""
    endpoints = [
        ("get", f"{BASE_URL}/", None),
        ("post", f"{BASE_URL}/", {"email": True}),
        ("get", f"{BASE_URL}/1/", None),
        ("put", f"{BASE_URL}/1/", {"email": False}),
        ("delete", f"{BASE_URL}/1/", None),
    ]

    for method, url, data in endpoints:
        response = getattr(api_client, method)(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_other_user_access(user1, test_settings, api_client):
    """Тест доступа к чужим настройкам."""

    api_client.force_authenticate(user=user1)

    response = api_client.get(f"{BASE_URL}/{test_settings.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
