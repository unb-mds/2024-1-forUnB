from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.Logout_view, name='logout'),
]
# urlpatterns = [
#     path('register/', views.register_unb_email, name='register_unb_email'),
# ]