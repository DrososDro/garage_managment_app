from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import Permissions


def send_activation_mail(request, user):
    curent_site = get_current_site(request)
    uidb = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    site = f"http://{curent_site.domain}/activate/{uidb}/{token}/"

    mail_subject = "Activate account for Our Site"
    message = f"""
    Welcome {user.email} in our Site #sitename
    Click the folowing link to activate your account

    {site}

    if this email is now for you please delete it.
    """
    send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )