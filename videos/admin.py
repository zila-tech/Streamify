from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "uploaded_at")
    search_fields = ("title", "description", "created_by__email")
    list_filter = ("uploaded_at", "created_by")
    readonly_fields = ("uploaded_at",)

    fieldsets = (
        (None, {"fields": ("title", "description", "video_file")}),
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


admin.site.register(Video, VideoAdmin)
