from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Anime, AnimeMangaMapping, Manga


class HomeSearchRecommendationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.anime = Anime.objects.create(
            title="Jujutsu Kaisen",
            original_title="주술회전",
            poster_image_url="https://example.com/jujutsu-anime.jpg",
            status=Anime.WorkStatus.COMPLETED,
            release_year=2020,
            rating_avg=4.7,
            favorite_count=100,
        )
        self.manga = Manga.objects.create(
            title="Jujutsu Kaisen",
            original_title="주술회전",
            cover_image_url="https://example.com/jujutsu-manga.jpg",
            status=Manga.MangaStatus.ONGOING,
            rating_avg=4.8,
            favorite_count=120,
        )
        self.mapping = AnimeMangaMapping.objects.create(
            anime=self.anime,
            manga=self.manga,
            anime_season_label="Season 1",
            anime_episode_from=1,
            anime_episode_to=24,
            continue_volume=8,
            continue_chapter=64,
            mapping_text="애니 1기 이후 원작 만화 8권 64화부터",
        )

    def test_home_api_returns_initial_sections(self):
        response = self.client.get(reverse("works:home"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("recommended_mappings", response.data)
        self.assertIn("popular_animes", response.data)
        self.assertIn("popular_mangas", response.data)
        self.assertEqual(response.data["recommended_mappings"][0]["id"], self.mapping.id)

    def test_search_api_returns_grouped_results(self):
        response = self.client.get(reverse("works:search"), {"keyword": "주술"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["keyword"], "주술")
        self.assertEqual(response.data["animes"][0]["id"], self.anime.id)
        self.assertEqual(response.data["mangas"][0]["id"], self.manga.id)
        self.assertEqual(response.data["mappings"][0]["id"], self.mapping.id)

    def test_search_api_returns_400_without_keyword(self):
        response = self.client.get(reverse("works:search"))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recommendations_api_returns_mapping_cards(self):
        response = self.client.get(reverse("works:mapping-recommendations"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.mapping.id)
        self.assertEqual(
            response.data["results"][0]["mapping_text"],
            self.mapping.mapping_text,
        )
