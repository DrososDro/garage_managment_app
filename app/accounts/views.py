from rest_framework import generics
from accounts.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create the user Here.
    Please put a valid email and check your mails for
    the validation email
    """

    serializer_class = UserSerializer
