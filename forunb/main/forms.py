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
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm mt-2 fw-bold input-title',
                'placeholder': 'Titulo'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mt-2 fw-bold',
                'placeholder': 'Escreva sua pergunta...'
            })
        }
        

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



