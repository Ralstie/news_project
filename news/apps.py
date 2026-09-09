"""Application configuration for the NewsHub application."""

from django.apps import AppConfig


class NewsConfig(AppConfig):
    """Configure the NewsHub Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    def ready(self):
        """Import signal handlers when the application starts."""
        import news.signals
