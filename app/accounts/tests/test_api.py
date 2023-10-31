from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest

from rest_framework.test import APIClient
from rest_framework import status

pytestmark = pytest.mark.django_db


CREATE_USER_URL = reverse("accounts:create_user")
client = APIClient()


# -------------------- Test create User from Api --------------------
def test_create_user_from_api_should_succeed(def_user):
    """Test Create a user from the api and
    check if he is Inactive"""

    res = client.post(CREATE_USER_URL, def_user)

    assert res.status_code == status.HTTP_201_CREATED

    user = get_user_model().objects.get(email=def_user["email"])
    assert user.check_password(def_user["password"]) is True
    assert user.is_active is False


def test_create_user_with_the_same_email_should_fail(create_user, def_user):
    """Test create a user with the same email should fail"""

    create_user(**def_user)
    res = client.post(CREATE_USER_URL, def_user)

    assert res.status_code == status.HTTP_400_BAD_REQUEST

    error_message = "user with this email address already exists."
    assert error_message == str(res.data["email"][0])
