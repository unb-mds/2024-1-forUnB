from django import forms
from .models import Forum, Answer
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description']
        labels = {
            'title': '',
            'description': ''
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

def validate_unb_email(value):
    if not value.endswith('@aluno.unb.br'):
        raise ValidationError('Por favor, utilize um email da UNB válido.')

class UnbEmailRegistrationForm(forms.Form):
    email = forms.EmailField(label='Email UNB', validators=[validate_unb_email])
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Verifica se o email já está em uso por outro usuário
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está cadastrado.')
        return email
