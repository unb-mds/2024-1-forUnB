from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.Logout_view, name='logout'),
]
# urlpatterns = [
#     path('register/', views.register_unb_email, name='register_unb_email'),
# ]