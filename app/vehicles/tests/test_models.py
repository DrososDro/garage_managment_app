import pytest
from unittest.mock import patch
from django.db.utils import IntegrityError
from vehicles.models import (
    VehiclesCategoriesBase,
    VehicleFamily,
    VehicleBrand,
    VehicleModel,
    vehicle_image_path,
)

pytestmark = pytest.mark.django_db

# -------------------- Test vehicle Family --------------------


def test_create_a_vehicle_brand_without_image_sould_succeed():
    """Test create a vehicle brand without image should succeed"""
    vehicle = VehicleBrand.objects.create(name="Audi")
    assert str(vehicle) == "Audi"
    assert VehicleBrand.objects.filter(name="Audi").exists() is True


def test_create_a_vehicle_brand_with_existing_name_without_image_sould_fail():
    """Test create vehicle brand with same name should throw IntegrityError"""
    VehicleBrand.objects.create(name="Audi")
    with pytest.raises(IntegrityError):
        VehicleBrand.objects.create(name="Audi")


@patch("vehicles.models.uuid.uuid4")
def test_create_vehicle_with_file_should_succeed(patched_uuid):
    """TEst create vehicle brand with wrong file should fail"""
    patched_uuid.return_value = "test"
    vehicle_path = vehicle_image_path(None, "vehicle.jpg")

    assert vehicle_path == "uploads/vehicle_categories/test.jpg"


def test_inherit_from_vehicles_categories_base():
    """Test if vehicles brand inherits from VehiclesCategoriesBase"""
    vehicle = VehicleBrand.objects.create(name="Audi")
    assert isinstance(vehicle, VehiclesCategoriesBase)


# -------------------- Test vehicle Family --------------------


def test_vehicle_Family_should_succeed():
    """Test the vehicle family should succeed
    because is inherits from  VehiclesCategoriesBase only
    we test if is isnstance"""

    family = VehicleFamily.objects.create(name="Family")
    assert isinstance(family, VehiclesCategoriesBase)


# -------------------- Test vehicle Model --------------------


def test_vehicle_Model_should_succeed():
    """Test the vehicle model should succeed
    because is inherits from  VehiclesCategoriesBase only
    we test if is isnstance"""

    veh_model = VehicleModel.objects.create(name="Family")
    assert isinstance(veh_model, VehiclesCategoriesBase)


def test_vehicle_model_add_vehicle_brand():
    """Test create a vehicle model with brand and family"""
    vehicle_brand = VehicleBrand.objects.create(name="Audi")
    vehicle_family = VehicleFamily.objects.create(name="road")
    veh_model = VehicleModel.objects.create(
        name="a4", brand=vehicle_brand, family=vehicle_family
    )
    assert veh_model.family == vehicle_family
    assert veh_model.brand == vehicle_brand


def test_vehicle_model_without_family_brand_should_succeed():
    """Test create VehicleModel without family and brand should succeed"""
    veh_model = VehicleModel.objects.create(name="a4")

    assert len(VehicleModel.objects.all()) == 1
