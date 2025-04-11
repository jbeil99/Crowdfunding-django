from django.urls import path, include, re_path
from .views import UserDonations

urlpatterns = [
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.jwt")),
    path(
        "api/users/<int:pk>/donations", UserDonations.as_view(), name="user-donations"
    ),
]
