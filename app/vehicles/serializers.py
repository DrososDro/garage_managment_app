from vehicles.models import VehicleFamily, VehicleBrand, VehicleModel
from rest_framework import serializers


class VehicleFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleFamily
        fields = ["name", "image", "id"]
        read_only_fields = ["id"]


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = ["name", "image", "id"]
        read_only_fields = ["id"]


class VehicleModelSerializer(serializers.ModelSerializer):
    family = VehicleFamilySerializer(read_only=True)
    brand = VehicleBrandSerializer(read_only=True)
    brands = serializers.ChoiceField(
        choices=(),
        required=False,
        write_only=True,
    )

    families = serializers.ChoiceField(
        choices=(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = VehicleModel
        fields = ["name", "id", "image", "brand", "family", "families", "brands"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "brands": {
                "write_only": True,
            }
        }

    def create(self, validated_data):
        brands = validated_data.pop("brands", None)
        family = validated_data.pop("families", None)
        obj = VehicleModel.objects.create(**validated_data)
        if brands:
            vh_brand, _ = VehicleBrand.objects.get_or_create(name=brands)
            obj.brand = vh_brand
        if family:
            vh_fam, _ = VehicleFamily.objects.get_or_create(name=family)
            obj.family = vh_fam
        obj.save()
        return obj

    def get_fields(self):
        field = super().get_fields()
        brands_choices = VehicleBrand.objects.values_list("name", flat=True)
        families_choices = VehicleFamily.objects.values_list("name", flat=True)

        field["brands"].choices = brands_choices or ["default"]
        field["families"].choices = families_choices or ["default"]

        return field
