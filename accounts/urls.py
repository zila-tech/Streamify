from django.urls import path
from accounts.views import (
    userregistrationview,
    activateaccountview,
    loginview,
    logoutview,
    forgotpasswordview,
    passwordresetcompleteview,
    passwordresetconfirmview,
    updateaccountview,
)


app_name = "auth"
urlpatterns = [
    path("signup/", userregistrationview, name="signup"),
    path("activate/<uidb64>/<token>/", activateaccountview, name="activate"),
    path("login/", loginview, name="login"),
    path("logout/", logoutview, name="logout"),
    path("forgot-password/", forgotpasswordview, name="forgotPassword"),
    path(
        "reset-password/<uidb64>/<token>/",
        passwordresetconfirmview,
        name="password_reset_confirm",
    ),
    path(
        "reset-password-complete/",
        passwordresetcompleteview,
        name="password_reset_complete",
    ),
    path(
        "profile/",
        updateaccountview,
        name="profile",
    ),
]
