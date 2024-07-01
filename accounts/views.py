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
    success_url = reverse_lazy("auth:login")

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
        self.compose_email(form, user, "account_verification_email.html")

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


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(Account, pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, _("Congratulations! Your account is activated."))
            return redirect("auth:login")
        else:
            messages.error(request, _("Invalid activation link"))
            return redirect("auth:register")


activateaccountview = ActivateAccountView.as_view()


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("auth:user_dashboard")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = auth.authenticate(email=username, password=password)
        if user is not None:
            auth.login(self.request, user)
            messages.success(self.request, _("You are now logged in."))
            return super().form_valid(form)
        else:
            messages.error(self.request, _("Invalid login credentials."))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Invalid form submission."))
        return self.render_to_response(self.get_context_data(form=form))


loginview = LoginView.as_view()


class LogoutView(CustomPermissionMixin, View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, _("You are logged out."))
        return redirect("auth:login")


logoutview = LogoutView.as_view()
