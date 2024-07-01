from django.urls import path
from .views import userregistrationview

app_name = "auth"
urlpatterns = [
    path("signup/", userregistrationview, name="signup"),
]
