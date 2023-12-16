from os import walk
import pytest
from django.urls import reverse, resolve
from rest_framework import status
from vehicles.views import BaseVehiclesFamilyViewset

from vehicles.models import VehicleBrand, VehicleFamily, VehicleModel

pytestmark = pytest.mark.django_db

VEHICLE_FAMILY_URL = reverse("vehicles:vehiclefamily-list")
VEHICLE_BRAND_URL = reverse("vehicles:vehiclebrand-list")
VEHICLE_MODEL_URL = reverse("vehicles:vehiclemodel-list")


def vehicle_family_url_with_id(id):
    return reverse("vehicles:vehiclefamily-detail", args=[id])


def vehicle_model_rev_id(id):
    return reverse("vehicles:vehiclemodel-detail", args=[id])


def vehicle_brand_rev_url(id):
    return reverse("vehicles:vehiclebrand-detail", args=[id])


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
    res = client.post(VEHICLE_FAMILY_URL, payload)
    assert res.status_code == result
    family = VehicleFamily.objects.all()
    assert len(family) == data_len
    if data_len:
        assert "/media/uploads/vehicle_categories/" in res.data["image"]
        assert "audi" in res.data["name"]

        res = client.delete(vehicle_family_url_with_id(res.data.get("id")))
        assert res.status_code == status.HTTP_204_NO_CONTENT


#
# @pytest.mark.parametrize(
#     "perm,result,data_len",
#     [
#         ("admin", status.HTTP_200_OK, 1),
#         ("garaze_admin", status.HTTP_200_OK, 1),
#         ("technician", status.HTTP_403_FORBIDDEN, 0),
#         ("customer", status.HTTP_403_FORBIDDEN, 0),
#         ("b2b", status.HTTP_403_FORBIDDEN, 0),
#     ],
# )
# def test_vehicle_family_put(
#     auth_client,
#     perm,
#     result,
#     data_len,
#     create_vehicle_family,
# ):
#     """Test vehicle put"""
#     family = create_vehicle_family
#     client = auth_client(perm=perm)
#     payload = {"name": "suzuki", "image": temporary_image()}
#     if data_len:
#         res = client.put(
#             vehicle_family_url_with_id(family.id), payload, format="multipart"
#         )
#     else:
#         res = client.put(VEHICLE_FAMILY_URL, payload)
#     assert res.status_code == result
#     family = VehicleFamily.objects.all()
#
#     if data_len:
#         assert res.data["name"] == family[0].name
#         family[0].image.delete()
#


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


# @pytest.mark.parametrize(
#     "perm,result,data_len",
#     [
#         ("admin", status.HTTP_200_OK, 1),
#         ("garaze_admin", status.HTTP_200_OK, 1),
#         ("technician", status.HTTP_200_OK, 1),
#         ("customer", status.HTTP_403_FORBIDDEN, 0),
#         ("b2b", status.HTTP_403_FORBIDDEN, 0),
#     ],
# )
# def test_vehicle_family_get_details(
#     auth_client,
#     perm,
#     result,
#     data_len,
#     create_vehicle_family,
# ):
#     """Test vehicle get_details"""
#     family = create_vehicle_family
#     client = auth_client(perm=perm)
#     res = client.get(vehicle_family_url_with_id(family.id))
#     assert res.status_code == result
#


def test_families_is_subclass_of_BaseFamilies():
    """Test if families is subclass go base families"""
    resolve_cls = resolve(VEHICLE_FAMILY_URL).func.cls
    assert issubclass(resolve_cls, BaseVehiclesFamilyViewset)


def test_brand_is_subclass_of_BaseFamilies():
    """Test if brand is subclass go base families"""
    resolve_cls = resolve(VEHICLE_BRAND_URL).func.cls
    assert issubclass(resolve_cls, BaseVehiclesFamilyViewset)


def test_model_is_subclass_of_BaseFamilies():
    """Test if model is subclass go base families"""
    resolve_cls = resolve(VEHICLE_MODEL_URL).func.cls
    assert issubclass(resolve_cls, BaseVehiclesFamilyViewset)


def test_model_get_method_details_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to create family and brand tags"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "families": "test",
        "brands": "brand",
    }
    req = client.post(VEHICLE_MODEL_URL, payload, format="multipart")
    assert req.status_code == status.HTTP_201_CREATED
    res = client.get(VEHICLE_MODEL_URL)
    assert res.status_code == status.HTTP_200_OK
    assert "A4" == res.data[0]["name"]
    assert "test" == res.data[0]["family"]["name"]
    assert "brand" == res.data[0]["brand"]["name"]

    res = client.delete(vehicle_model_rev_id(res.data[0].get("id")))
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_post_method_create_with_family_and_brand_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to create family and brand tags"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "families": "test",
        "brands": "brand",
    }
    res = client.post(VEHICLE_MODEL_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_201_CREATED
    assert "A4" == res.data["name"]

    res = client.delete(vehicle_model_rev_id(res.data.get("id")))
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_post_method_create_with_brand_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to create brand tags"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "brands": "brand",
    }
    res = client.post(VEHICLE_MODEL_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_201_CREATED
    assert "A4" == res.data["name"]

    res = client.delete(vehicle_model_rev_id(res.data.get("id")))
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_post_method_create_with_family_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to create family  tags"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "families": "test",
    }
    res = client.post(VEHICLE_MODEL_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_201_CREATED
    assert "A4" == res.data["name"]

    res = client.delete(vehicle_model_rev_id(res.data.get("id")))
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_post_method_create_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to create tags"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.post(VEHICLE_MODEL_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_201_CREATED
    assert "A4" == res.data["name"]

    res = client.delete(vehicle_model_rev_id(res.data.get("id")))
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_patch_method_with_family_and_brand_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to patch family and brand tags"""
    vh_model = VehicleModel.objects.create(name="machine")
    REV_URL = vehicle_model_rev_id(vh_model.id)

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "families": "test",
        "brands": "brand",
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    assert "A4" == res.data["name"]

    res = client.delete(REV_URL)
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_patch_method_with_brand_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to patch brand tags"""
    vh_model = VehicleModel.objects.create(name="machine")
    REV_URL = vehicle_model_rev_id(vh_model.id)

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "brands": "brand",
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    assert "A4" == res.data["name"]

    res = client.delete(REV_URL)
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_patch_method_with_family_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to patch family  tags"""
    vh_model = VehicleModel.objects.create(
        name="machine",
    )
    REV_URL = vehicle_model_rev_id(vh_model.id)

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "families": "test",
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    assert "A4" == res.data["name"]

    res = client.delete(REV_URL)
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_model_patch_method_create_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to patch model"""
    vh_model = VehicleModel.objects.create(name="machine")
    REV_URL = vehicle_model_rev_id(vh_model.id)

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    assert "A4" == res.data["name"]

    res = client.delete(REV_URL)
    assert res.status_code == status.HTTP_204_NO_CONTENT


# def test_model_put_method_with_family_and_brand_should_succeed(
#     auth_client,
# ):
#     """Test the vehicle model should able to patch family and brand tags"""
#     vh_model = VehicleModel.objects.create(name="machine")
#     REV_URL = vehicle_model_rev_id(vh_model.id)
#
#     client = auth_client(perm="admin")
#
#     payload = {
#         "name": "A4",
#         "image": temporary_image(),
#         "families": "test",
#         "brands": "brand",
#     }
#     res = client.put(REV_URL, payload, format="multipart")
#     assert res.status_code == status.HTTP_200_OK
#     assert "A4" == res.data["name"]


# def test_model_put_method_with_brand_should_succeed(
#     auth_client,
# ):
#     """Test the vehicle model should able to patch brand tags"""
#     vh_model = VehicleModel.objects.create(name="machine")
#     REV_URL = vehicle_model_rev_id(vh_model.id)
#
#     client = auth_client(perm="admin")
#
#     payload = {
#         "name": "A4",
#         "image": temporary_image(),
#         "brands": "brand",
#     }
#     res = client.put(REV_URL, payload, format="multipart")
#     assert res.status_code == status.HTTP_200_OK
#     assert "A4" == res.data["name"]
#
#
# def test_model_put_method_with_family_should_succeed(
#     auth_client,
# ):
#     """Test the vehicle model should able to patch family  tags"""
#     vh_model = VehicleModel.objects.create(name="machine")
#     REV_URL = vehicle_model_rev_id(vh_model.id)
#
#     client = auth_client(perm="admin")
#
#     payload = {
#         "name": "A4",
#         "image": temporary_image(),
#         "families": "test",
#     }
#     res = client.put(REV_URL, payload, format="multipart")
#     assert res.status_code == status.HTTP_200_OK
#     assert "A4" == res.data["name"]
#


# def test_model_put_method_create_should_succeed(
#     auth_client,
# ):
#     """Test the vehicle model should able to patch model"""
#     vh_model = VehicleModel.objects.create(name="machine")
#     REV_URL = vehicle_model_rev_id(vh_model.id)
#
#     client = auth_client(perm="admin")
#
#     payload = {
#         "name": "A4",
#         "image": temporary_image(),
#     }
#     res = client.put(REV_URL, payload, format="multipart")
#     assert res.status_code == status.HTTP_200_OK
#     assert "A4" == res.data["name"]


def test_model_delete_method_with_brand_should_succeed(
    auth_client,
):
    """Test the vehicle model should able to patch brand tags"""
    vh_model = VehicleModel.objects.create(name="machine")
    REV_URL = vehicle_model_rev_id(vh_model.id)

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
        "brands": "brand",
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    assert "A4" == res.data["name"]

    res = client.delete(REV_URL)
    assert VehicleBrand.objects.filter(name="brand").exists() is True
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_update_image_brand_delete_old(auth_client):
    """Test the update brand image that is deleted after the update"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.post(VEHICLE_BRAND_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_201_CREATED
    model = VehicleBrand.objects.get(pk=res.data["id"])
    img = model.image.url
    REV_URL = vehicle_brand_rev_url(model.id)

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    res = client.get(img)
    assert res.status_code == status.HTTP_404_NOT_FOUND

    res = client.delete(REV_URL)
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_update_image_family_delete_old(auth_client):
    """Test the update family image that is deleted after the update"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.post(VEHICLE_FAMILY_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_201_CREATED
    model = VehicleFamily.objects.get(pk=res.data["id"])
    img = model.image.url
    REV_URL = vehicle_family_url_with_id(model.id)

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    res = client.get(img)
    assert res.status_code == status.HTTP_404_NOT_FOUND

    res = client.delete(REV_URL)
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_update_image_model_delete_old(auth_client):
    """Test the update model image that is deleted after the update"""

    client = auth_client(perm="admin")

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.post(VEHICLE_MODEL_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_201_CREATED
    model = VehicleModel.objects.get(pk=res.data["id"])
    img = model.image.url
    REV_URL = vehicle_model_rev_id(model.id)

    payload = {
        "name": "A4",
        "image": temporary_image(),
    }
    res = client.patch(REV_URL, payload, format="multipart")
    assert res.status_code == status.HTTP_200_OK
    res = client.get(img)
    assert res.status_code == status.HTTP_404_NOT_FOUND

    res = client.delete(REV_URL)
    assert res.status_code == status.HTTP_204_NO_CONTENT
