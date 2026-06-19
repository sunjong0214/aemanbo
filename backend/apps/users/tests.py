from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            nickname="테스트유저",
            email="test@example.com",
            password="testpass1234",
        )

    def test_profile_api_requires_authentication(self):
        response = self.client.get(reverse("users:my-profile"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_get_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse("users:my-profile"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["nickname"], "테스트유저")
        self.assertEqual(response.data["email"], "test@example.com")

    def test_authenticated_user_can_update_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse("users:my-profile"),
            {
                "nickname": "수정된닉네임",
                "profile_image_url": "https://example.com/profile.jpg",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], "수정된닉네임")
        self.assertEqual(
            response.data["profile_image_url"],
            "https://example.com/profile.jpg",
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, "수정된닉네임")

    def test_profile_api_does_not_allow_role_update(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse("users:my-profile"),
            {
                "role": User.Role.ADMIN,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.Role.USER)