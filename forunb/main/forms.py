from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description']
        labels = {
            'title': '',
            'description': ''
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        labels = {
            'text': ''
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80})
        }

User = get_user_model()



