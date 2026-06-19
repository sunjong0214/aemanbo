from django.contrib import admin

from .models import (
    Anime,
    AnimeMangaMapping,
    AnimeTag,
    Manga,
    MangaEpisode,
    MangaTag,
    MetadataTag,
)


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "type",
        "status",
        "studio",
        "release_year",
        "episode_count",
        "rating_avg",
        "favorite_count",
    )
    list_filter = ("status", "type", "studio", "release_year")
    search_fields = ("title", "original_title", "studio")
    ordering = ("title",)


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "author",
        "publisher",
        "rating_avg",
        "favorite_count",
    )
    list_filter = ("status", "publisher")
    search_fields = ("title", "original_title", "author", "publisher")
    ordering = ("title",)


@admin.register(MangaEpisode)
class MangaEpisodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "manga",
        "volume_number",
        "chapter_number",
        "title",
        "published_at",
        "rating_avg",
    )
    list_filter = ("manga", "volume_number")
    search_fields = ("manga__title", "title")
    ordering = ("manga", "volume_number", "chapter_number")


@admin.register(AnimeMangaMapping)
class AnimeMangaMappingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "anime",
        "manga",
        "anime_season_label",
        "anime_episode_from",
        "anime_episode_to",
        "continue_volume",
        "continue_chapter",
        "mapping_text",
    )
    list_filter = ("anime", "manga", "anime_season_label")
    search_fields = ("anime__title", "manga__title", "mapping_text")
    ordering = ("anime", "anime_episode_from", "id")


@admin.register(MetadataTag)
class MetadataTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    list_filter = ("type",)
    search_fields = ("name",)
    ordering = ("type", "name")


@admin.register(AnimeTag)
class AnimeTagAdmin(admin.ModelAdmin):
    list_display = ("id", "anime", "tag")
    list_filter = ("tag__type",)
    search_fields = ("anime__title", "tag__name")


@admin.register(MangaTag)
class MangaTagAdmin(admin.ModelAdmin):
    list_display = ("id", "manga", "tag")
    list_filter = ("tag__type",)
    search_fields = ("manga__title", "tag__name")