import pytest
from django.urls import reverse, resolve
from rest_framework import status
from vehicles.views import BaseVehiclesFamilyViewset

from vehicles.models import VehicleFamily

pytestmark = pytest.mark.django_db

VEHICLE_FAMILY_URL = reverse("vehicles:vehiclefamily-list")


def vehicle_family_url_with_id(id):
    return reverse("vehicles:vehiclefamily-detail", args=[id])


# -------------------- test  vehicle Family apis --------------------
def temporary_image():
    import tempfile
    from PIL import Image

    image = Image.new("RGB", (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg", prefix="test_img_")
    image.save(tmp_file, "jpeg")
    tmp_file.seek(0)
    return tmp_file


@pytest.mark.parametrize(
    "perm,result,data_res",
    [
        ("admin", status.HTTP_200_OK, 0),
        ("garaze_admin", status.HTTP_200_OK, 0),
        ("technician", status.HTTP_200_OK, 0),
        ("customer", status.HTTP_403_FORBIDDEN, 1),
        ("b2b", status.HTTP_403_FORBIDDEN, 1),
    ],
)
def test_vehicle_family_get_list_(
    auth_client,
    perm,
    result,
    data_res,
):
    """Test vehicle get list"""
    client = auth_client(perm=perm)
    res = client.get(VEHICLE_FAMILY_URL)
    assert res.status_code == result
    assert len(res.data) == data_res


@pytest.mark.parametrize(
    "perm,result,data_len",
    [
        ("admin", status.HTTP_201_CREATED, 1),
        ("garaze_admin", status.HTTP_201_CREATED, 1),
        ("technician", status.HTTP_403_FORBIDDEN, 0),
        ("customer", status.HTTP_403_FORBIDDEN, 0),
        ("b2b", status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_vehicle_family_post(
    auth_client,
    perm,
    result,
    data_len,
):
    """Test vehicle family post"""
    client = auth_client(perm=perm)
    payload = {"name": "audi", "image": temporary_image()}
    res = client.post(VEHICLE_FAMILY_URL, payload, format="multipart")
    assert res.status_code == result
    family = VehicleFamily.objects.all()
    assert len(family) == data_len
    if data_len:
        assert "/media/uploads/vehicle_categories/" in res.data["image"]
        assert "audi" in res.data["name"]

        family[0].image.delete()


@pytest.mark.parametrize(
    "perm,result,data_len",
    [
        ("admin", status.HTTP_200_OK, 1),
        ("garaze_admin", status.HTTP_200_OK, 1),
        ("technician", status.HTTP_403_FORBIDDEN, 0),
        ("customer", status.HTTP_403_FORBIDDEN, 0),
        ("b2b", status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_vehicle_family_put(
    auth_client,
    perm,
    result,
    data_len,
    create_vehicle_family,
):
    """Test vehicle put"""
    family = create_vehicle_family
    client = auth_client(perm=perm)
    payload = {"name": "suzuki", "image": temporary_image()}
    if data_len:
        res = client.put(
            vehicle_family_url_with_id(family.id), payload, format="multipart"
        )
    else:
        res = client.put(VEHICLE_FAMILY_URL, payload)
    assert res.status_code == result
    family = VehicleFamily.objects.all()

    if data_len:
        assert res.data["name"] == family[0].name
        family[0].image.delete()


@pytest.mark.parametrize(
    "perm,result,data_len",
    [
        ("admin", status.HTTP_200_OK, 1),
        ("garaze_admin", status.HTTP_200_OK, 1),
        ("technician", status.HTTP_403_FORBIDDEN, 0),
        ("customer", status.HTTP_403_FORBIDDEN, 0),
        ("b2b", status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_vehicle_family_patch(
    auth_client,
    perm,
    result,
    data_len,
    create_vehicle_family,
):
    """Test vehicle patch"""
    family = create_vehicle_family
    client = auth_client(perm=perm)
    payload = {"name": "suzuki"}
    if data_len:
        res = client.patch(vehicle_family_url_with_id(family.id), payload)
    else:
        res = client.patch(VEHICLE_FAMILY_URL, payload)
    assert res.status_code == result
    if data_len:
        assert res.data["name"] == "suzuki"


@pytest.mark.parametrize(
    "perm,result,data_len",
    [
        ("admin", status.HTTP_204_NO_CONTENT, 1),
        ("garaze_admin", status.HTTP_204_NO_CONTENT, 1),
        ("technician", status.HTTP_403_FORBIDDEN, 0),
        ("customer", status.HTTP_403_FORBIDDEN, 0),
        ("b2b", status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_vehicle_family_delete(
    auth_client,
    perm,
    result,
    data_len,
    create_vehicle_family,
):
    """Test vehicle delete"""
    client = auth_client(perm=perm)
    payload = {"name": "audi", "image": temporary_image()}
    family = client.post(VEHICLE_FAMILY_URL, payload, format="multipart")
    if data_len:
        res = client.delete(vehicle_family_url_with_id(family.data["id"]))
    else:
        res = client.delete(VEHICLE_FAMILY_URL)
    assert res.status_code == result


@pytest.mark.parametrize(
    "perm,result,data_len",
    [
        ("admin", status.HTTP_200_OK, 1),
        ("garaze_admin", status.HTTP_200_OK, 1),
        ("technician", status.HTTP_200_OK, 1),
        ("customer", status.HTTP_403_FORBIDDEN, 0),
        ("b2b", status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_vehicle_family_get_details(
    auth_client,
    perm,
    result,
    data_len,
    create_vehicle_family,
):
    """Test vehicle get_details"""
    family = create_vehicle_family
    client = auth_client(perm=perm)
    res = client.get(vehicle_family_url_with_id(family.id))
    assert res.status_code == result


def test_families_is_instance_of_BaseFamilies():
    resolve_cls = resolve(VEHICLE_FAMILY_URL).func.cls
    assert issubclass(resolve_cls, BaseVehiclesFamilyViewset)
