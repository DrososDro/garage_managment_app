from django.urls import include, path
from rest_framework.routers import DefaultRouter
from vehicles import views

router = DefaultRouter()
router.register("familys", views.VehicleFamilyViewSets)
# router.register("brand", views.VehicleBrandViewSets)
# router.register("model", views.VehicleModelViewSets)


app_name = "vehicles"
urlpatterns = [path("", include(router.urls))]
