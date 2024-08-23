"""URL configurations for the search application."""

from django.urls import path
from search import views

app_name = "search"  # pylint: disable=C0103

urlpatterns = [
    path('search/', views.search_forum, name='search_forum'),
]
