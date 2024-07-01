from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, View, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .mixins import CustomPermissionMixin
from .utils import MailUtils
from .forms import LoginForm, RegistrationForm, SetPasswordForm
from .models import Account
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


class UserRegistrationView(MailUtils, CreateView):
    model = Account
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("auth:signup")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        password = form.cleaned_data.get("password")
        user.password = make_password(password)
        user.save()

        group, created = Group.objects.get_or_create(name="Users")
        if created:
            group.save()

        user.groups.add(group)

        # Send activation email
        self.composeEmail(form, user)

        messages.success(
            self.request,
            _("Please confirm your email address to complete the registration."),
        )

        return redirect(self.success_url)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, _(f"{field}: {error}"))
        return super().form_invalid(form)


userregistrationview = UserRegistrationView.as_view()
