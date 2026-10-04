
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def _is_assistant(user):
    return user.groups.filter(name='Assistant').exists()


def assistant_required(view):
    """Only logged-in users in the 'Assistant' group may access the view."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not _is_assistant(request.user):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper


def patient_required(view):
    """Only logged-in users who have a Patient profile may access the view."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not hasattr(request.user, 'patient'):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper