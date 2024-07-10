import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Video


@receiver(pre_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
    # Delete the video file
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)

    # Delete the thumbnail
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)


@receiver(pre_save, sender=Video)
def delete_old_files_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_video = Video.objects.get(pk=instance.pk)
    except Video.DoesNotExist:
        return False

    # Check if video_file has changed
    if old_video.video_file and old_video.video_file != instance.video_file:
        if os.path.isfile(old_video.video_file.path):
            os.remove(old_video.video_file.path)

    # Check if thumbnail has changed
    if old_video.thumbnail and old_video.thumbnail != instance.thumbnail:
        if os.path.isfile(old_video.thumbnail.path):
            os.remove(old_video.thumbnail.path)
