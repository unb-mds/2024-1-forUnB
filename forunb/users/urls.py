"""URL configurations for the users application."""

from django.urls import path
from . import views

app_name = "users"  # pylint: disable=C0103

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # URL para editar perfil
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('verify-email/', views.verify_email, name='verify_email'),
]

# urlpatterns = [
#     path('register/', views.register_unb_email, name='register_unb_email'),
# ]
