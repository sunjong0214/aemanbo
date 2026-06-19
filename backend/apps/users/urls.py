from django.urls import path

from .views import UserProfileAPIView

app_name = "users"

urlpatterns = [
    path("me/profile/", UserProfileAPIView.as_view(), name="my-profile"),
]