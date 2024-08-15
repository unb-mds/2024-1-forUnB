"""App configuration for the search application."""

from django.apps import AppConfig


class SearchConfig(AppConfig):
    """Configuration class for the search app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    