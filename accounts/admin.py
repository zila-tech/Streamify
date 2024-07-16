from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import Account
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Streamify Administration")
admin.site.site_title = _("Streamify Admin Portal")
admin.site.index_title = _("Welcome to the Streamify Admin Portal")

@admin.register(Account)
class AccountAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Account
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "gender",
        "last_login",
        "date_joined",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "gender",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "email",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_admin",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "gender",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_admin",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
