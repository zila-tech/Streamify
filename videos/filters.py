import django_filters
from .models import Video
from django import forms


class VideoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by Title","type":"search"}
        ),
    )

    class Meta:
        model = Video
        fields = ["title"]
