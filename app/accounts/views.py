from django.contrib.auth import get_user_model
from django.contrib.auth.forms import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status, views, viewsets
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from accounts.models import Permissions


class CreateUserView(generics.CreateAPIView):
    """
    Create the user Here.
    Please put a valid email and check your mails for
    the validation email
    """

    serializer_class = UserSerializer


class ActivateEmail(views.APIView):
    """Activate Email address and take the basic Permission."""

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            get_user_model().DoesNotExist,
        ):
            user = None
        if user is not None and default_token_generator.check_token(
            user,
            token,
        ):
            user.is_active = True
            user.save()
            perm, created = Permissions.objects.get_or_create(name="customer")
            user.permissions.add(perm)

            return Response(data="Activations Success")
        else:
            return Response(
                data="Activation Fail",
                status=status.HTTP_400_BAD_REQUEST,
            )
