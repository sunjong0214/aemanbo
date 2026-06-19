from django.db.models import Q

from .models import Anime, AnimeMangaMapping, Manga


DEFAULT_SEARCH_LIMIT = 10
DEFAULT_RECOMMENDATION_LIMIT = 20
MAX_RECOMMENDATION_LIMIT = 50


def get_home_data():
    return {
        "recommended_mappings": get_recommended_mappings(limit=6),
        "popular_animes": Anime.objects.order_by(
            "-favorite_count",
            "-rating_avg",
            "title",
        )[:6],
        "popular_mangas": Manga.objects.order_by(
            "-favorite_count",
            "-rating_avg",
            "title",
        )[:6],
    }


def search_works(keyword, limit=DEFAULT_SEARCH_LIMIT):
    normalized_keyword = keyword.strip()
    if not normalized_keyword:
        raise ValueError("keyword is required")

    anime_query = (
        Q(title__icontains=normalized_keyword)
        | Q(original_title__icontains=normalized_keyword)
        | Q(studio__icontains=normalized_keyword)
        | Q(synopsis__icontains=normalized_keyword)
    )
    manga_query = (
        Q(title__icontains=normalized_keyword)
        | Q(original_title__icontains=normalized_keyword)
        | Q(author__icontains=normalized_keyword)
        | Q(illustrator__icontains=normalized_keyword)
        | Q(publisher__icontains=normalized_keyword)
        | Q(description__icontains=normalized_keyword)
    )
    mapping_query = (
        Q(mapping_text__icontains=normalized_keyword)
        | Q(description__icontains=normalized_keyword)
        | Q(source_note__icontains=normalized_keyword)
        | Q(anime__title__icontains=normalized_keyword)
        | Q(anime__original_title__icontains=normalized_keyword)
        | Q(manga__title__icontains=normalized_keyword)
        | Q(manga__original_title__icontains=normalized_keyword)
    )

    return {
        "keyword": normalized_keyword,
        "animes": Anime.objects.filter(anime_query).order_by(
            "-favorite_count",
            "-rating_avg",
            "title",
        )[:limit],
        "mangas": Manga.objects.filter(manga_query).order_by(
            "-favorite_count",
            "-rating_avg",
            "title",
        )[:limit],
        "mappings": AnimeMangaMapping.objects.select_related(
            "anime",
            "manga",
        )
        .filter(mapping_query)
        .order_by("-created_at", "-id")[:limit],
    }


def get_recommended_mappings(limit=DEFAULT_RECOMMENDATION_LIMIT):
    safe_limit = max(1, min(limit, MAX_RECOMMENDATION_LIMIT))
    return AnimeMangaMapping.objects.select_related("anime", "manga").order_by(
        "-created_at",
        "-id",
    )[:safe_limit]
