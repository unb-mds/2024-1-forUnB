"""Forms module for managing user-related forms and validations."""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import Question, Answer
from .models import CustomUser


def validate_unb_email(value):
    """Validator to ensure the email provided is a valid UnB email."""
    if not value.endswith('@aluno.unb.br'):
        raise ValidationError('Por favor, utilize um email da UnB válido.')


class CustomUserCreationForm(UserCreationForm):  # pylint: disable=R0901
    """Form for creating a new user with additional email validation."""

    email = forms.EmailField(validators=[validate_unb_email])

    class Meta: # pylint: disable=C0115, R0903
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_username(self):
        """Ensure the username is unique."""
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_email(self):
        """Ensure the email is unique and belongs to UnB."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email já cadastrado.')
        if not email.endswith('@aluno.unb.br'):
            raise ValidationError('Por favor, utilize um email válido da UnB.')
        return email

    def save(self, commit=True):
        """Save the user with a cleaned username."""
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Form for updating an existing user with additional fields."""

    class Meta: # pylint: disable=C0115, R0903
        model = CustomUser
        fields = (
            'email', 'username', 'followed_forums', 'liked_questions', 'liked_answers',
            'created_questions', 'created_answers', 'is_active', 'is_staff'
        )
        field_classes = {
            'created_questions': forms.ModelMultipleChoiceField,
            'created_answers': forms.ModelMultipleChoiceField,
        }

    created_questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(), required=False # pylint: disable=E1101
    )
    created_answers = forms.ModelMultipleChoiceField(
        queryset=Answer.objects.all(), required=False # pylint: disable=E1101
    )


class ProfileEditForm(forms.ModelForm):
    """Form for editing the user's profile with basic fields."""

    class Meta: # pylint: disable=C0115, R0903
        model = CustomUser
        fields = ['username', 'photo']

    def clean_username(self):
        """Ensure the username is unique except for the current user."""
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username
