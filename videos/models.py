from django.db import models

from accounts.models import Account


class Video(models.Model):
    """
    Model representing a video.

    Attributes:
        title (str): Title of the video.
        description (str): Description of the video.
        video_file (FileField): The video file.
        created_by (ForeignKey): The user who upload the video
        uploaded_at (datetime): The date and time when the video was uploaded.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to="videos/")
    created_by  = models.ForeignKey(
        Account,
        related_name="owner",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
