from django.contrib import admin
from .models import Video
from django.utils.html import format_html


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "uploaded_at", "thumbnail_preview")
    search_fields = ("title", "description", "created_by__email")
    list_filter = ("uploaded_at", "created_by")
    readonly_fields = ("uploaded_at", "thumbnail_preview")

    fieldsets = (
        (None, {"fields": ("title", "description", "video_file", "thumbnail")}),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("created_by", "uploaded_at"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />',
                obj.thumbnail.url,
            )
        return "No thumbnail"

    thumbnail_preview.short_description = "Thumbnail Preview"


admin.site.register(Video, VideoAdmin)
