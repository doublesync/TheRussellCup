from functools import wraps

from django.shortcuts import render

from simulation.config import CONFIG_SEASON


def check_free_agency_open(view_func):
    """
    Decorator to check if free agency is open.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not CONFIG_SEASON["FREE_AGENCY_OPEN"]:
            # Render the 500.html template instead of returning None
            return render(
                request, "500.html", {"reason": "❌ Free agency is not open."}
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
