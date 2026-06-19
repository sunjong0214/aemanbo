from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Anime, AnimeMangaMapping, AnimeTag, Manga, MangaEpisode, MangaTag, MetadataTag


class DetailMappingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.anime = Anime.objects.create(
            title="주술회전",
            original_title="呪術廻戦",
            poster_image_url="https://example.com/jujutsu-poster.jpg",
            banner_image_url="https://example.com/jujutsu-banner.jpg",
            type=Anime.AnimeType.TVA,
            release_year=2020,
            episode_count=24,
            status=Anime.WorkStatus.COMPLETED,
            studio="MAPPA",
            synopsis="저주를 둘러싼 싸움을 그린 다크 판타지 애니메이션.",
            rating_avg=4.7,
            rating_count=120,
            favorite_count=50,
        )
        self.manga = Manga.objects.create(
            title="주술회전",
            original_title="呪術廻戦",
            cover_image_url="https://example.com/jujutsu-cover.jpg",
            banner_image_url="https://example.com/jujutsu-manga-banner.jpg",
            author="아쿠타미 게게",
            publisher="슈에이샤",
            description="저주와 주술사를 중심으로 전개되는 배틀 만화.",
            status=Manga.MangaStatus.ONGOING,
            rating_avg=4.8,
            rating_count=180,
            favorite_count=70,
        )

        action = MetadataTag.objects.create(name="액션", type=MetadataTag.TagType.GENRE)
        dark_fantasy = MetadataTag.objects.create(
            name="다크 판타지",
            type=MetadataTag.TagType.GENRE,
        )
        studio = MetadataTag.objects.create(name="MAPPA", type=MetadataTag.TagType.STUDIO)

        AnimeTag.objects.create(anime=self.anime, tag=action)
        AnimeTag.objects.create(anime=self.anime, tag=dark_fantasy)
        AnimeTag.objects.create(anime=self.anime, tag=studio)

        MangaTag.objects.create(manga=self.manga, tag=action)
        MangaTag.objects.create(manga=self.manga, tag=dark_fantasy)

        self.episode = MangaEpisode.objects.create(
            manga=self.manga,
            volume_number=8,
            chapter_number=64,
            title="시부야 사변",
            rating_avg=4.8,
        )

        self.mapping = AnimeMangaMapping.objects.create(
            anime=self.anime,
            manga=self.manga,
            anime_season_label="Season 1",
            anime_episode_from=1,
            anime_episode_to=24,
            manga_volume_from=1,
            manga_volume_to=8,
            manga_chapter_from=1,
            manga_chapter_to=63,
            continue_volume=8,
            continue_chapter=64,
            mapping_text="애니 1기 이후 원작 만화 8권 64화부터",
            description="애니 1기는 원작 63화까지를 다룹니다.",
            source_note="테스트 데이터",
        )

    def test_anime_detail_api_returns_anime(self):
        url = reverse("works:anime-detail", args=[self.anime.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.anime.id)
        self.assertEqual(response.data["title"], "주술회전")
        self.assertEqual(len(response.data["tags"]), 3)

    def test_anime_detail_api_returns_404_for_missing_anime(self):
        url = reverse("works:anime-detail", args=[99999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Anime not found.")

    def test_anime_manga_mappings_api_returns_mappings(self):
        url = reverse("works:anime-manga-mappings", args=[self.anime.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["anime_id"], self.anime.id)
        self.assertEqual(len(response.data["mappings"]), 1)
        self.assertEqual(
            response.data["mappings"][0]["mapping_text"],
            "애니 1기 이후 원작 만화 8권 64화부터",
        )
        self.assertEqual(response.data["mappings"][0]["manga"]["id"], self.manga.id)

    def test_manga_detail_api_returns_manga(self):
        url = reverse("works:manga-detail", args=[self.manga.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.manga.id)
        self.assertEqual(response.data["title"], "주술회전")
        self.assertEqual(len(response.data["tags"]), 2)

    def test_manga_detail_api_returns_404_for_missing_manga(self):
        url = reverse("works:manga-detail", args=[99999])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Manga not found.")

    def test_manga_episodes_api_returns_episodes(self):
        url = reverse("works:manga-episodes", args=[self.manga.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["manga_id"], self.manga.id)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["chapter_number"], 64)

    def test_manga_episodes_api_filters_by_volume(self):
        MangaEpisode.objects.create(
            manga=self.manga,
            volume_number=9,
            chapter_number=65,
            title="다음 에피소드",
            rating_avg=4.5,
        )
        url = reverse("works:manga-episodes", args=[self.manga.id])

        response = self.client.get(url, {"volume": 8})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["volume_number"], 8)

    def test_manga_anime_mappings_api_returns_mappings(self):
        url = reverse("works:manga-anime-mappings", args=[self.manga.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["manga_id"], self.manga.id)
        self.assertEqual(len(response.data["mappings"]), 1)
        self.assertEqual(response.data["mappings"][0]["anime"]["id"], self.anime.id)
        self.assertEqual(
            response.data["mappings"][0]["mapping_text"],
            "애니 1기 이후 원작 만화 8권 64화부터",
        )