import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models import Permissions
from vehicles.models import VehicleFamily


@pytest.fixture
def auth_client():
    def inner(perm="admin"):
        """Api client force authenticate"""
        user = get_user_model().objects.create_user(
            "user@example.com",
            "password123",
        )
        user.is_activate = True
        user.save()
        permission = Permissions.objects.create(name=perm)
        user.permissions.add(permission)
        client = APIClient()
        client.force_authenticate(user)
        return client

    return inner


@pytest.fixture
def create_vehicle_family():
    return VehicleFamily.objects.create(name="Tractor")
