from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    Configuration for the News application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "news"
