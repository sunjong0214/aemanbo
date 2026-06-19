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


class AnimeTagInline(admin.TabularInline):
    model = AnimeTag
    extra = 1
    autocomplete_fields = ("tag",)


class MangaTagInline(admin.TabularInline):
    model = MangaTag
    extra = 1
    autocomplete_fields = ("tag",)


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
    readonly_fields = ("created_at", "updated_at")
    inlines = (AnimeTagInline,)
    fieldsets = (
        (
            "Basic",
            {
                "fields": (
                    "title",
                    "original_title",
                    "type",
                    "status",
                    "release_year",
                    "episode_count",
                    "studio",
                )
            },
        ),
        ("Images", {"fields": ("poster_image_url", "banner_image_url")}),
        ("Content", {"fields": ("synopsis",)}),
        ("Stats", {"fields": ("rating_avg", "rating_count", "favorite_count")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


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
    readonly_fields = ("created_at", "updated_at")
    inlines = (MangaTagInline,)
    fieldsets = (
        (
            "Basic",
            {
                "fields": (
                    "title",
                    "original_title",
                    "status",
                    "author",
                    "illustrator",
                    "publisher",
                )
            },
        ),
        ("Images", {"fields": ("cover_image_url", "banner_image_url")}),
        ("Content", {"fields": ("description",)}),
        ("Stats", {"fields": ("rating_avg", "rating_count", "favorite_count")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )


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
    autocomplete_fields = ("manga",)
    list_select_related = ("manga",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(AnimeMangaMapping)
class AnimeMangaMappingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "anime",
        "manga",
        "anime_season_label",
        "anime_episode_range",
        "manga_chapter_range",
        "anime_episode_from",
        "anime_episode_to",
        "continue_volume",
        "continue_chapter",
        "mapping_text",
    )
    list_filter = ("anime_season_label", "anime", "manga")
    search_fields = (
        "anime__title",
        "anime__original_title",
        "manga__title",
        "manga__original_title",
        "mapping_text",
        "source_note",
    )
    ordering = ("anime", "anime_episode_from", "id")
    autocomplete_fields = ("anime", "manga")
    list_select_related = ("anime", "manga")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Works", {"fields": ("anime", "manga", "anime_season_label")}),
        (
            "Anime Range",
            {"fields": ("anime_episode_from", "anime_episode_to")},
        ),
        (
            "Manga Range",
            {
                "fields": (
                    "manga_volume_from",
                    "manga_volume_to",
                    "manga_chapter_from",
                    "manga_chapter_to",
                )
            },
        ),
        ("Continue From", {"fields": ("continue_volume", "continue_chapter")}),
        ("Display", {"fields": ("mapping_text", "description", "source_note")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Anime episodes", ordering="anime_episode_from")
    def anime_episode_range(self, obj):
        if obj.anime_episode_from and obj.anime_episode_to:
            return f"{obj.anime_episode_from}-{obj.anime_episode_to}"
        if obj.anime_episode_from:
            return f"{obj.anime_episode_from}+"
        return "-"

    @admin.display(description="Manga chapters", ordering="manga_chapter_from")
    def manga_chapter_range(self, obj):
        chapter_from = obj.manga_chapter_from
        chapter_to = obj.manga_chapter_to
        volume_from = obj.manga_volume_from
        volume_to = obj.manga_volume_to

        volume_label = "-"
        if volume_from and volume_to:
            volume_label = f"v{volume_from}-v{volume_to}"
        elif volume_from:
            volume_label = f"v{volume_from}+"

        if chapter_from and chapter_to:
            return f"{volume_label} / ch{chapter_from}-{chapter_to}"
        if chapter_from:
            return f"{volume_label} / ch{chapter_from}+"
        return volume_label


@admin.register(MetadataTag)
class MetadataTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    list_filter = ("type",)
    search_fields = ("name",)
    ordering = ("type", "name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(AnimeTag)
class AnimeTagAdmin(admin.ModelAdmin):
    list_display = ("id", "anime", "tag")
    list_filter = ("tag__type",)
    search_fields = ("anime__title", "tag__name")
    autocomplete_fields = ("anime", "tag")
    list_select_related = ("anime", "tag")


@admin.register(MangaTag)
class MangaTagAdmin(admin.ModelAdmin):
    list_display = ("id", "manga", "tag")
    list_filter = ("tag__type",)
    search_fields = ("manga__title", "tag__name")
    autocomplete_fields = ("manga", "tag")
    list_select_related = ("manga", "tag")
