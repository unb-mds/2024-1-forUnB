from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('questions/', views.questions, name='questions'),
    path('questions/<question_id>/', views.question, name='question'),
    path('new_question/', views.new_question, name='new_question'),
    path('new_answer/<question_id>/', views.new_answer, name='new_answer'),
]