from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

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
