"""
Serializer for the account model
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    """Serializer fot the user Model."""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """Create the user with the validated_data"""
        return get_user_model().objects.create_user(**validated_data)