"""URL configurations for the users application."""

from django.urls import path
from . import views

APP_NAME = "users"  # Conform to UPPER_CASE naming style

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # URL para editar perfil
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
]

# urlpatterns = [
#     path('register/', views.register_unb_email, name='register_unb_email'),
# ]
