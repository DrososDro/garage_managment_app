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

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.serializer_class, list):
            for serializer in self.serializer_class:
                if "Details" in serializer.__name__:
                    details_serializer = serializer
                else:
                    other_serializer = serializer

            if self.action == "retrieve":
                ("details", details_serializer)
                self.serializer_class = details_serializer
            else:
                self.serializer_class = other_serializer

        return super().get_serializer(*args, **kwargs)


class VehicleFamilyViewSets(BaseVehiclesFamilyViewset):
    """viewset for VehicleFamily"""

    serializer_class = [
        serializers.VehicleFamilySerializer,
        serializers.VehicleFamilyDetailsSerializer,
    ]
    queryset = VehicleFamily.objects.all()


class VehicleBrandViewSets(BaseVehiclesFamilyViewset):
    """Viewset for VehicleBrand"""

    serializer_class = [
        serializers.VehicleBrandSerializer,
        serializers.VehicleBrandDetailsSerializer,
    ]
    queryset = VehicleBrand.objects.all()


#
class VehicleModelViewSets(BaseVehiclesFamilyViewset):
    serializer_class = [
        serializers.VehicleModelSerializer,
        serializers.VehicleModelDetailsSerializer,
    ]
    queryset = VehicleModel.objects.all()
