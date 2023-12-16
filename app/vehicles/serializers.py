from vehicles.models import VehicleFamily, VehicleBrand, VehicleModel, Vehicle
from rest_framework import serializers


class VehicleFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleFamily
        fields = ["name", "image", "id"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        image = validated_data.get("image")
        if image is not None:
            instance.image.delete()

        return super().update(instance, validated_data)


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = ["name", "image", "id"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        image = validated_data.get("image")
        if image is not None:
            instance.image.delete()

        return super().update(instance, validated_data)


class VehicleModelSerializer(serializers.ModelSerializer):
    family = VehicleFamilySerializer(read_only=True)
    brand = VehicleBrandSerializer(read_only=True)
    brands = serializers.CharField(
        required=False,
        write_only=True,
    )

    families = serializers.CharField(
        required=False,
        write_only=True,
    )

    class Meta:
        model = VehicleModel
        fields = [
            "name",
            "id",
            "image",
            "brand",
            "family",
            "families",
            "brands",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "brands": {"write_only": True},
            "families": {"write_only": True},
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

    def update(self, instance, validated_data):
        brands = validated_data.pop("brands", None)
        family = validated_data.pop("families", None)
        image = validated_data.get("image")
        if image is not None:
            instance.image.delete()
        if brands:
            vh_brand, _ = VehicleBrand.objects.get_or_create(name=brands)
            instance.brand = vh_brand
        if family:
            vh_fam, _ = VehicleFamily.objects.get_or_create(name=family)
            instance.family = vh_fam
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
