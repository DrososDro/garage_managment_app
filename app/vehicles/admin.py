from django.contrib import admin
from vehicles.models import (
    VehicleFamily,
    VehicleBrand,
    VehicleModel,
)

# Register your models here.


admin.site.register(VehicleModel)
admin.site.register(VehicleBrand)
admin.site.register(VehicleFamily)
