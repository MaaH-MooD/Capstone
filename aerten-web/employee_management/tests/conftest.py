from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import pytest

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False, user=None):
        User = get_user_model()
        if user is None:
            user = User.objects.create_user(
                username='testuser',
                password='testpass123',
                is_staff=is_staff
            )
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate