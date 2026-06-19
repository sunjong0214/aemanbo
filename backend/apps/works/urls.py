from django.urls import path

from .views import (
    AnimeDetailAPIView,
    AnimeMangaMappingsAPIView,
    HomeAPIView,
    MangaAnimeMappingsAPIView,
    MangaDetailAPIView,
    MangaEpisodesAPIView,
    MappingRecommendationsAPIView,
    SearchAPIView,
)

app_name = "works"

urlpatterns = [
    path("home/", HomeAPIView.as_view(), name="home"),
    path("search/", SearchAPIView.as_view(), name="search"),
    path(
        "mappings/recommendations/",
        MappingRecommendationsAPIView.as_view(),
        name="mapping-recommendations",
    ),
    path("animes/<int:anime_id>/", AnimeDetailAPIView.as_view(), name="anime-detail"),
    path(
        "animes/<int:anime_id>/manga-mappings/",
        AnimeMangaMappingsAPIView.as_view(),
        name="anime-manga-mappings",
    ),
    path("mangas/<int:manga_id>/", MangaDetailAPIView.as_view(), name="manga-detail"),
    path(
        "mangas/<int:manga_id>/episodes/",
        MangaEpisodesAPIView.as_view(),
        name="manga-episodes",
    ),
    path(
        "mangas/<int:manga_id>/anime-mappings/",
        MangaAnimeMappingsAPIView.as_view(),
        name="manga-anime-mappings",
    ),
]
