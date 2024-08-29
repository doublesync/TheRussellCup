# Django imports
from django.urls import path

# Local imports
from pages.views import home, google_adsense

# URLs
urlpatterns = [
    path("", home, name="home"),
    path("ads.txt", google_adsense, name="google_adsense"),
]
