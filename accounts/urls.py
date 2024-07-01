from django.urls import path
from .views import userregistrationview, activateaccountview, loginview, logoutview

app_name = "auth"
urlpatterns = [
    path("signup/", userregistrationview, name="signup"),
    path("activate/<uidb64>/<token>/", activateaccountview, name="activate"),
    path("login/", loginview, name="login"),
    path("logout/", logoutview, name="logout"),
]

