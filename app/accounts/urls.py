from django.urls import path
from accounts import views

app_name = "accounts"
urlpatterns = [
    path(
        "create-user/",
        views.CreateUserView.as_view(),
        name="create_user",
    ),
    path("activate/<uidb64>/<token>/", views.ActivateEmail.as_view(), name="activate"),
]
