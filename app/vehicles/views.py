from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from vehicles.models import VehicleBrand, VehicleFamily, VehicleModel
from vehicles import serializers
from rest_framework.permissions import IsAuthenticated
from core.perm_class import UserPermissions


class BaseVehiclesFamilyViewset(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        VIEW_ACTION_LIST = {"list", "retrieve"}

        if self.action in VIEW_ACTION_LIST:
            return (
                IsAuthenticated(),
                UserPermissions(
                    perm_list={
                        "technician",
                        "admin",
                        "garaze_admin",
                    }
                )(),
            )
        else:
            return (
                IsAuthenticated(),
                UserPermissions(
                    perm_list={
                        "admin",
                        "garaze_admin",
                    }
                )(),
            )


class VehicleFamilyViewSets(BaseVehiclesFamilyViewset):
    """viewset for VehicleFamily"""

    serializer_class = serializers.VehicleFamilySerializer
    queryset = VehicleFamily.objects.all()


# class VehicleBrandViewSets(BaseVehiclesFamilySerializer):
#     serializer_class = serializers.VehicleBrandSerializer
#     queryset = VehicleBrand.objects.all()
#
#
# class VehicleModelViewSets(BaseVehiclesFamilySerializer):
#     serializer_class = serializers.VehicleModelSerializer
#     queryset = VehicleModel.objects.all()
