import pytest
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.urls import reverse

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


def test_create_user_with_len_pass_9_should_succed(def_user):
    """Test create user with len pass of 9 should succed"""
    def_user["password"] = "test123xp"

    res = client.post(CREATE_USER_URL, def_user)

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["email"] == def_user["email"]


def test_create_user_with_len_pass_7_should_fail(def_user):
    """Test create user with len pass of 7 should fail"""
    def_user["password"] = "test123"

    res = client.post(CREATE_USER_URL, def_user)

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@patch("accounts.serializers.send_activation_mail")
def test_create_user_send_activation_email_should_call(
    patched_activation_mail, def_user
):
    """Test create user and func send activation email sould called once"""
    patched_activation_mail.return_value = True

    res = client.post(CREATE_USER_URL, def_user)

    assert res.status_code == status.HTTP_201_CREATED

    assert patched_activation_mail.call_count == 1


@patch("accounts.serializers.send_activation_mail")
def test_create_user_fail_send_email_shouldnt_call(
    patched_activation_mail,
    def_user,
    create_user,
):
    """Test create existing user should fail and email dont send"""
    create_user(**def_user)
    res = client.post(CREATE_USER_URL, def_user)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    patched_activation_mail.return_value = False

    assert patched_activation_mail.call_count == 0
