from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_forum, name='search_forum'),
]