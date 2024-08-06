from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # URL para editar perfil
    path('register/', views.register, name='register'),
    path('logout/', views.Logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
]
# urlpatterns = [
#     path('register/', views.register_unb_email, name='register_unb_email'),
# ]
