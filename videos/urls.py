from django.urls import path
from .views import home, videodetailview, getprevnextidsview

urlpatterns = [
    path("", home, name="home"),
    path("videos/<int:pk>/", videodetailview, name="video-detail"),
    path(
        "videos/get-prev-next-ids/<int:pk>/",
        getprevnextidsview,
        name="get-prev-next-ids",
    ),
]
