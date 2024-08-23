""" This file contains the forms used in the application. """

from django import forms
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Forum, Question, Answer, Report


class ForumForm(forms.ModelForm):
    """ Form to create a forum. """
    class Meta:  # pylint: disable=R0903
        """ Meta class for ForumForm. """
        model = Forum
        fields = ['title', 'description']
        labels = {
            'title': '',
            'description': '',
        }


class QuestionForm(forms.ModelForm):
    """ Form to create a question. """
    class Meta:  # pylint: disable=R0903
        """ Meta class for QuestionForm. """
        model = Question
        fields = ['title', 'description', 'is_anonymous', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'texto form-control form-control-sm mt-2 input-title',
                'placeholder': 'Titulo',
            }),
            'description': forms.Textarea(attrs={
                'id': 'id_description',
                'class': 'texto descricao form-control mt-2',
                'placeholder': 'Escreva sua pergunta...',
                'rows': 5,
                'cols': 50,
            }),
        }
        labels = {
            'is_anonymous': 'Modo anônimo'
        }


class AnswerForm(forms.ModelForm):
    """ Form to create an answer. """
    class Meta:  # pylint: disable=R0903
        """ Meta class for AnswerForm. """
        model = Answer
        fields = ['text', 'is_anonymous', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'id': 'id_answer_text',
                'class': 'texto descricao form-control mt-2',
                'placeholder': 'Escreva sua resposta...',
                'rows': 5,
                'cols': 50,
            }),
        }
        labels = {
            'text': ''
        }


User = get_user_model()


class ReportForm(forms.ModelForm):
    """ Form to report a question or answer. """
    class Meta:  # pylint: disable=R0903
        """ Meta class for ReportForm. """
        model = Report
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.RadioSelect,
            'details': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Detalhes adicionais (opcional)'}),
        }
        labels = {
            'reason': 'Motivo da denúncia',
            'details': 'Detalhes adicionais',
        }
