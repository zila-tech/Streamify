from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Video
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Video


class VideoListView(ListView):
    model = Video
    template_name = "videos/home.html"
    # template_name = "videos/video-details.html"
    context_object_name = "videos"
    ordering = ["-date_posted"]
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_root"] = "Home"
        return context


home = VideoListView.as_view()


class VideoDetailView(ListView):
    model = Video
    template_name = "videos/video-details.html"
    context_object_name = "videos"
    ordering = ["-date_posted"]
    paginate_by = 9

    def get_single_object(self):
        # Fetch the video using the primary key from the URL
        return get_object_or_404(Video, pk=self.kwargs["pk"])

    def get_queryset(self):
        # Exclude the single video from the list of other videos
        queryset = super().get_queryset()
        single_video = self.get_single_object()
        return queryset.exclude(pk=single_video.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_root"] = "Video Details"
        context["video"] = self.get_single_object()
        return context


videodetailview = VideoDetailView.as_view()


class GetPrevNextIDsView(View):
    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        all_videos = Video.objects.order_by("-date_posted")
        videos_list = list(all_videos)
        current_index = videos_list.index(video)

        prev_video_id = videos_list[current_index - 1].id if current_index > 0 else None
        next_video_id = (
            videos_list[current_index + 1].id
            if current_index < len(videos_list) - 1
            else None
        )

        return JsonResponse(
            {
                "prev_video_id": prev_video_id,
                "next_video_id": next_video_id,
            }
        )


getprevnextidsview = GetPrevNextIDsView.as_view()
# def home(request):
# return render(request, "videos/home.html")
# return render(request, "videos/video-details.html")
