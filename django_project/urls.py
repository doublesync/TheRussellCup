from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("users/", include("accounts.urls")),
    path("players/", include("players.urls")),
    path("teams/", include("teams.urls")),
    path("news/", include("news.urls")),
    path("logs/", include("logs.urls")),
    path("stafftools/", include("stafftools.urls")),
    path("stats/", include("stats.urls")),
    path("", include("pages.urls")),
    
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
