from django import forms
from videos.models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description", "video_file", "thumbnail"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter video title", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter video description",
                    "class": "form-control",
                    "rows": 5,
                }
            ),
            "video_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_video_file(self):
        video_file = self.cleaned_data["video_file"]
        # Maximum file size validation (100 MB)
        max_size = 100 * 1024 * 1024  # 100 MB in bytes
        if video_file.size > max_size:
            raise forms.ValidationError(
                f"File size is too large (max size is {max_size/(1024*1024)} MB)"
            )

        # Allowed file types validation (example for MP4 files)
        allowed_types = ["video/mp4"]
        if video_file.content_type not in allowed_types:
            raise forms.ValidationError("Only MP4 files are allowed.")

        return video_file


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description", "video_file", "thumbnail"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter video title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter video description",
                }
            ),
            "video_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "thumbnail": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
