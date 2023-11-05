from vehicles.models import VehicleFamily, VehicleBrand, VehicleModel
from rest_framework import serializers


class VehicleFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleFamily
        fields = ["name", "image", "id"]
        read_only_fields = ["id"]


# class VehicleBrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VehicleBrand
#         fields = ["name", "image", "id"]
#         read_only_fields = ["id"]
#
#
# class VehicleModelSerializer(serializers.ModelSerializer):
#     family = VehicleFamilySerializer(required=False)
#     brand = VehicleBrandSerializer(required=False)
#
#     class Meta:
#         model = VehicleBrand
#         fields = ["name", "image", "id", "family", "brand"]  #
#         read_only_fields = ["id"]
