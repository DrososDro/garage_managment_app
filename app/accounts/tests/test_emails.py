"""
Tests for the email in utils
"""
from unittest.mock import patch
from django.urls import reverse
from django.views.decorators.debug import HttpRequest
import pytest
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db
request = HttpRequest()


CREATE_USER_URL = reverse("accounts:create_user")
client = APIClient()


@patch("accounts.utils.get_current_site")
def test_send_creation_email_should_succeed(
    patched_site, mailoutbox, settings, def_user
):
    """Test send creation email with correct data"""
    patched_site.domain.return_value = "xaos"
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    mail_subject = "Activate account for Our Site"
    site = "/activate/"

    assert len(mailoutbox) == 0
    res = client.post(CREATE_USER_URL, def_user)

    assert res.status_code == status.HTTP_201_CREATED
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == mail_subject
    assert site in str(mailoutbox[0].body)
