from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('questions/', views.questions, name='questions'),
    path('forums/', views.forum_list, name='forum_list'),
    path('new_question/<int:forum_id>/', views.new_question, name='new_question'),
    path('new_answer/<int:question_id>/', views.new_answer, name='new_answer'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('search.urls')),
]