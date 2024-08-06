from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from main.models import *

def validate_unb_email(value):
    if not value.endswith('@aluno.unb.br'):
        raise ValidationError('Por favor, utilize um email da UNB válido.')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_unb_email])

    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Define o username como o email
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'followed_forums', 'liked_questions', 'created_questions', 'created_answers', 'is_active', 'is_staff')
        field_classes = {
            'created_questions': forms.ModelMultipleChoiceField,
            'created_answers': forms.ModelMultipleChoiceField,
        }
    created_questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), required=False)
    created_answers = forms.ModelMultipleChoiceField(queryset=Answer.objects.all(), required=False)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.user_id).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username