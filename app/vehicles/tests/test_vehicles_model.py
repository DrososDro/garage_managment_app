import pytest


pytestmark = pytest.mark.django_db
from vehicles.models import Vehicle
from django.db.utils import IntegrityError


def test_create_vehicle_should_succeed(create_vehicle_model):
    """Test create vehicle with correct data"""
    veh_model = create_vehicle_model
    payload = {
        "vin": "12345Ab",
        "plate_number": "nki3521",
        "model_id": "620",
        "engine_number": "engine",
        "vehicle_model": veh_model,
    }
    veh = Vehicle.objects.create(**payload)

    veh.refresh_from_db()
    assert veh.vin == payload["vin"]
    assert veh.plate_number == payload["plate_number"]
    assert veh.model_id == payload["model_id"]
    assert veh.engine_number == payload["engine_number"]
    assert veh.vehicle_model == veh_model


def test_create_vehicle_without_vehicle_model_should_succeed(create_vehicle_model):
    """Test create vehicle without vehicle_model"""
    veh_model = create_vehicle_model
    payload = {
        "vin": "12345Ab",
        "plate_number": "nki3521",
        "model_id": "620",
        "engine_number": "engine",
        "vehicle_model": veh_model,
    }
    veh = Vehicle.objects.create(**payload)

    veh.refresh_from_db()
    assert veh.vin == payload["vin"]
    assert veh.plate_number == payload["plate_number"]
    assert veh.model_id == payload["model_id"]
    assert veh.engine_number == payload["engine_number"]


def test_create_vehicle_with_existing_vin_should_fail():
    """Test create vehicle with existing vin"""

    payload = {
        "vin": "12345Ab",
        "plate_number": "nki3521",
        "model_id": "620",
        "engine_number": "engine",
    }
    Vehicle.objects.create(**payload)
    with pytest.raises(IntegrityError) as error:
        veh = Vehicle.objects.create(**payload)
    assert "duplicate key value violates unique constraint" in str(error.value)
