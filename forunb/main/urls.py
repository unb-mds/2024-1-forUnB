from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "main"

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('questions/', views.questions, name='questions'),
    path('user_posts/', views.user_posts, name='user_posts'),
    path('forums/', views.forum_list, name='forum_list'),
    path('new_question/<int:forum_id>/', views.new_question, name='new_question'),
    path('new_answer/<int:question_id>/', views.new_answer, name='new_answer'),
    path('follow-forum/<int:forum_id>/<str:action>/', views.follow_forum, name='follow_forum'),
    path('followed_forums/', views.followed_forums, name='followed_forums'),
    path('delete_question/<int:pk>/', views.delete_question, name='delete_question'),
    path('delete_answer/<int:pk>/', views.delete_answer, name='delete_answer'),
    path('notifications/', views.notifications, name='notifications'),
    path('toggle-upvote-question/<int:question_id>/', views.toggle_upvote_question, name='toggle_upvote_question'),
    path('toggle-upvote-answer/<int:answer_id>/', views.toggle_upvote_answer, name='toggle_upvote_answer'),
    # path('users/', include('users.urls')),  # Inclui as URLs do app 'users'
    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]