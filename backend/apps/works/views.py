from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Anime, AnimeMangaMapping, Manga, MangaEpisode
from .serializers import (
    AnimeDetailSerializer,
    AnimeMangaMappingSerializer,
    MangaDetailSerializer,
    MangaEpisodeSerializer,
)


class AnimeDetailAPIView(APIView):
    def get(self, request, anime_id):
        try:
            anime = Anime.objects.prefetch_related("tags").get(id=anime_id)
        except Anime.DoesNotExist:
            return Response(
                {"detail": "Anime not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AnimeDetailSerializer(anime)
        return Response(serializer.data)


class AnimeMangaMappingsAPIView(APIView):
    def get(self, request, anime_id):
        if not Anime.objects.filter(id=anime_id).exists():
            return Response(
                {"detail": "Anime not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        mappings = (
            AnimeMangaMapping.objects.select_related("anime", "manga")
            .filter(anime_id=anime_id)
            .order_by("anime_episode_from", "id")
        )
        serializer = AnimeMangaMappingSerializer(mappings, many=True)

        return Response(
            {
                "anime_id": anime_id,
                "mappings": serializer.data,
            }
        )


class MangaDetailAPIView(APIView):
    def get(self, request, manga_id):
        try:
            manga = Manga.objects.prefetch_related("tags").get(id=manga_id)
        except Manga.DoesNotExist:
            return Response(
                {"detail": "Manga not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MangaDetailSerializer(manga)
        return Response(serializer.data)


class MangaEpisodesAPIView(APIView):
    def get(self, request, manga_id):
        if not Manga.objects.filter(id=manga_id).exists():
            return Response(
                {"detail": "Manga not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        episodes = MangaEpisode.objects.filter(manga_id=manga_id)

        volume = request.query_params.get("volume")
        if volume:
            episodes = episodes.filter(volume_number=volume)

        serializer = MangaEpisodeSerializer(episodes, many=True)

        return Response(
            {
                "manga_id": manga_id,
                "count": episodes.count(),
                "results": serializer.data,
            }
        )


class MangaAnimeMappingsAPIView(APIView):
    def get(self, request, manga_id):
        if not Manga.objects.filter(id=manga_id).exists():
            return Response(
                {"detail": "Manga not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        mappings = (
            AnimeMangaMapping.objects.select_related("anime", "manga")
            .filter(manga_id=manga_id)
            .order_by("anime_id", "anime_episode_from", "id")
        )
        serializer = AnimeMangaMappingSerializer(mappings, many=True)

        return Response(
            {
                "manga_id": manga_id,
                "mappings": serializer.data,
            }
        )

