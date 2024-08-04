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
                'class': 'texto form-control form-control-sm mt-2 input-title',
                'placeholder': 'Titulo'
            }),
            'description': forms.Textarea(attrs={
                'class': 'texto descricao form-control mt-2',
                'placeholder': 'Escreva sua pergunta...',
                'rows': 5,  # Ajuste o número de linhas conforme necessário
                'cols': 50  # Ajuste o número de colunas conforme necessário
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



