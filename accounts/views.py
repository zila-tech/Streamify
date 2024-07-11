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

from accounts.mixins import ActiveUserRequiredMixin
from accounts.utils import MailUtils
from accounts.forms import (
    LoginForm,
    RegistrationForm,
    SetPasswordForm,
    UpdateAccountForm,
)
from accounts.models import Account
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash


class UserRegistrationView(MailUtils, CreateView):
    model = Account
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("auth:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user.username = str(email.split("@")[0])
        user.password = make_password(password)
        user.save()

        # Send activation email
        mail_temp = "accounts/account_verification_email.html"
        mail_subject = "Activate Your Account"
        self.compose_email(
            self.request, user, mail_subject=mail_subject, mail_temp=mail_temp
        )

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_root"] = "Sign Up"
        return context


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
            return redirect("auth:signup")


activateaccountview = ActivateAccountView.as_view()


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_root"] = "Login"
        return context


loginview = LoginView.as_view()


class LogoutView(ActiveUserRequiredMixin, View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, _("You are logged out."))
        return redirect("auth:login")


logoutview = LogoutView.as_view()


class ForgotPasswordView(MailUtils, View):
    template_name = "accounts/forgotPassword.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            mail_temp = "accounts/reset_password_email.html"
            mail_subject = "Reset Your Password"
            self.compose_email(
                self.request, user, mail_subject=mail_subject, mail_temp=mail_temp
            )
            messages.success(
                request, _("Password reset email has been sent to your email address.")
            )
            return redirect("auth:login")
        else:
            messages.error(request, _("Account does not exist!"))
            return redirect("auth:forgotPassword")


forgotpasswordview = ForgotPasswordView.as_view()


class PasswordResetConfirmView(AuthPasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("auth:password_reset_complete")

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            _(
                "Your password has been reset successfully. You can now log in with your new password."
            ),
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


passwordresetconfirmview = PasswordResetConfirmView.as_view()


class PasswordResetCompleteView(TemplateView):
    template_name = "accounts/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_root"] = _("Password Reset Complete - Breast Cancer Prediction")
        return context


passwordresetcompleteview = PasswordResetCompleteView.as_view()


class UpdateAccountView(ActiveUserRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Account, pk=request.user.pk)
        context = self.getContext(user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(Account, pk=request.user.pk)

        try:
            if "update_profile" in request.POST:
                form = UpdateAccountForm(request.POST, instance=user)
                form_type = "profile"
            elif "change_password" in request.POST:
                form = SetPasswordForm(user=user, data=request.POST)
                form_type = "password"

            if form.is_valid():
                form.save()
                if form_type == "password":
                    update_session_auth_hash(request, form.user)
                return redirect("auth:profile")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(self.request, f"{field}: {error}")
        except:
            messages.error(request, "Invalid form submission.")

        context = self.getContext(user)
        return render(request, self.template_name, context)

    def getContext(self, user):
        update_form = UpdateAccountForm(instance=user)
        password_form = SetPasswordForm(user=user)
        context = {
            "update_form": update_form,
            "password_form": password_form,
            "title_root": "Profile",
        }
        return context


updateaccountview = UpdateAccountView.as_view()
