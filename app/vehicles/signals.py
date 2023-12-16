from django.db.models.signals import post_delete, pre_delete

from vehicles.models import VehicleBrand, VehicleFamily, VehicleModel


# TODO: test the signals
def delete_photos(sender, instance, **kwargs):
    if instance.image:
        image = instance.image
        image.delete()


pre_delete.connect(delete_photos, sender=VehicleBrand)
pre_delete.connect(delete_photos, sender=VehicleModel)
pre_delete.connect(delete_photos, sender=VehicleFamily)
