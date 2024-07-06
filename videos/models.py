import random
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Video(models.Model):
    """
    Model representing a video.

    Attributes:
        title (str): Title of the video.
        description (str): Description of the video.
        video_file (FileField): The video file.
        created_by (ForeignKey): The user who uploaded the video.
        uploaded_at (datetime): The date and time when the video was uploaded.
    """

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    video_file = models.FileField(_("Video File"), upload_to="videos/")
    created_by = models.ForeignKey(
        "accounts.account",
        related_name="owner",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    thumbnail = models.ImageField(
        _("Thumbnail"), upload_to="thumbnails/", null=True, blank=True
    )
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return (
                settings.STATIC_URL
                + f"images/default_thumbnails/default_thumbnail-{random.randint(1, 5)}.jpg"
            )

    def __str__(self):
        return self.title
