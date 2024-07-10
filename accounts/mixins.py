from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

class ActiveUserRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and active."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_active:
            logout(request)
            messages.error(request, "Please log in to access this page.")
            return redirect("auth:login")
        return super().dispatch(request, *args, **kwargs)


