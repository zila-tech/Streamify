from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import Account
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm as AuthSetPasswordForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control ps-15 bg-transparent",
                "placeholder": "Enter Email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control ps-15 bg-transparent",
                "placeholder": "Enter Password",
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "gender",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "gender",
            "is_active",
            "is_staff",
            "is_admin",
            "groups",
            "user_permissions",
        )


class RegistrationForm(forms.ModelForm):

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "class": "form-control ps-15 bg-transparent",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirm_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
                "class": "form-control ps-15 bg-transparent",
            }
        ),
    )

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "password",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter First Name",
                    "class": "form-control ps-15 bg-transparent",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter Last Name",
                    "class": "form-control ps-15 bg-transparent",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter Email",
                    "class": "form-control ps-15 bg-transparent",
                }
            ),
            "gender": forms.Select(attrs={"class": "form-select ps-15 bg-transparent"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Account.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(confirm_password)
        return confirm_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control ps-15 bg-transparent",
                "placeholder": "Enter Email",
            }
        )
    )


class SetPasswordForm(AuthSetPasswordForm):
    """
    A form that lets a user set their password without entering the old
    password
    """

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control ps-15 bg-transparent",
                "placeholder": "New password",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control ps-15 bg-transparent",
                "placeholder": "New password confirmation",
            }
        ),
    )


class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "first_name",
            "last_name",
            "gender",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select ps-15 bg-transparent"}),
        }
