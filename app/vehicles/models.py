import os
import uuid
from django.db import models


# Create your models here.
def vehicle_image_path(instance, filename):
    """Return the path that the images of VehiclesCategoriesBase sould store"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "vehicle_categories", filename)


class VehiclesCategoriesBase(models.Model):
    """Base class for vehicles Categories."""

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=50, unique=True)
    image = models.FileField(null=True, upload_to=vehicle_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class VehicleFamily(VehiclesCategoriesBase):
    """Vehicle Family model
    stores the family of the vehicle
    like (forester, suv, tractor, truck)"""


class VehicleBrand(VehiclesCategoriesBase):
    """Vehicle Brands model
    stores the brand of the vehicle
    like (porsche, ferrari,benz, claas )"""


class VehicleModel(VehiclesCategoriesBase):
    """Vehicles Model model
    stores the model of the vehicle
    like (panamera, Amg, arion,)
    and have foreign keys to VehicleFamily, VehicleBrand
    because this are connected"""

    brand = models.ForeignKey(
        "VehicleBrand",
        on_delete=models.SET_NULL,
        null=True,
    )
    family = models.ForeignKey(
        "VehicleFamily",
        on_delete=models.SET_NULL,
        null=True,
    )


class Vehicle(models.Model):
    """Vehicle model"""

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    vin = models.CharField(max_length=200, unique=True)
    plate_number = models.CharField(unique=True, max_length=10)
    hp_or_cc = models.CharField(max_length=50)
    model_id = models.CharField(max_length=50)
    engine_number = models.CharField(max_length=50)
    # owner

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    vehicle_model = models.ForeignKey(
        VehicleModel, on_delete=models.SET_NULL, null=True
    )
