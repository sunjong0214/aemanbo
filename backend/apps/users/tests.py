from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class MyProfileAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="tester",
            nickname="tester",
            email="tester@example.com",
            password="password",
        )
        self.client.force_authenticate(user=self.user)

    def test_my_profile_api_returns_profile(self):
        response = self.client.get(reverse("users:me-profile"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "tester")
        self.assertEqual(response.data["nickname"], "tester")

    def test_my_profile_api_updates_profile(self):
        response = self.client.patch(
            reverse("users:me-profile"),
            {
                "nickname": "new-nickname",
                "profile_image_url": "https://example.com/profile.jpg",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], "new-nickname")
        self.assertEqual(
            response.data["profile_image_url"],
            "https://example.com/profile.jpg",
        )
