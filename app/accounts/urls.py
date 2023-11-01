from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "accounts"
urlpatterns = [
    path(
        "create-user/",
        views.CreateUserView.as_view(),
        name="create_user",
    ),
    path(
        "activate/<str:uidb64>/<str:token>/",
        views.ActivateEmail.as_view(),
        name="activate",
    ),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
