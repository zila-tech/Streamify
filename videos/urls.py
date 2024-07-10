from django.urls import path
from .views import (
    home,
    videodetailview,
    getprevnextidsview,
    getvideoview,
    addorupdatevideoview,
    videos,
    deletevideoview,
)


urlpatterns = [
    path("", home, name="home"),
    path("videos/<int:pk>/", videodetailview, name="video-detail"),
    path(
        "videos/get-prev-next-ids/<int:pk>/",
        getprevnextidsview,
        name="get-prev-next-ids",
    ),
    path("videos/mgt/", videos, name="videos"),
    path("add/", addorupdatevideoview, name="add_video"),
    path("update/<int:video_id>/", addorupdatevideoview, name="update_video"),
    path("get/<int:video_id>/", getvideoview, name="get_video"),
    path("delete-video/", deletevideoview, name="delete_video"),
]
