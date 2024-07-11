from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from accounts.mixins import ActiveUserRequiredMixin

from .filters import VideoFilter
from .models import Video
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Video
from .forms import VideoForm
from django.contrib import messages
from django_filters.views import FilterView


class VideoListView(ActiveUserRequiredMixin,FilterView):
    filterset_class = VideoFilter
    model = Video
    template_name = "videos/home.html"
    context_object_name = "videos"
    ordering = ["-date_posted"]
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_root"] = "Home"
        return context


home = VideoListView.as_view()


class Videos(ActiveUserRequiredMixin,FilterView):
    filterset_class = VideoFilter
    model = Video
    template_name = "videos/videos_list.html"
    context_object_name = "videos"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_root"] = "Videos"
        return context


videos = Videos.as_view()


class AddOrUpdateVideoView(ActiveUserRequiredMixin, View):
    form_class = VideoForm

    def post(self, request, *args, **kwargs):
        video_id = request.POST.get("video_id")
        if video_id:
            video = get_object_or_404(Video, id=video_id)
            form = self.form_class(request.POST, request.FILES, instance=video)
            msg = "updated"
        else:
            form = self.form_class(request.POST, request.FILES)
            msg = "created"

        if form.is_valid():
            video = form.save(commit=False)
            if not video_id:
                video.created_by = request.user
            video.save()
            messages.success(request, f"Video {msg} successfully.")
            return JsonResponse({"success": True})
        else:
            for error in form.errors:
                messages.error(request, f"Error {error}")
            return JsonResponse({"success": False, "errors": form.errors}, status=400)


addorupdatevideoview = AddOrUpdateVideoView.as_view()


class GetVideoView(ActiveUserRequiredMixin, View):
    def get(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(Video, id=video_id)
        data = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
        }
        return JsonResponse(data)


getvideoview = GetVideoView.as_view()


class DeleteVideoView(ActiveUserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        video_id = request.POST.get("video_id")
        video = get_object_or_404(Video, id=video_id)
        video.delete()
        messages.success(request, "Video deleted successfully.")
        return JsonResponse({"success": True, "message": "Video deleted successfully."})


deletevideoview = DeleteVideoView.as_view()


class VideoDetailView(ActiveUserRequiredMixin, FilterView):
    filterset_class = VideoFilter
    model = Video
    template_name = "videos/video-details.html"
    context_object_name = "videos"
    ordering = ["-date_posted"]
    paginate_by = 3

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


class GetPrevNextIDsView(ActiveUserRequiredMixin, View):
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
