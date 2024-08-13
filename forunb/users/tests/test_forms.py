from django.test import TestCase
from django.core.exceptions import ValidationError
from ..forms import CustomUserCreationForm, CustomUserChangeForm, ProfileEditForm
from ..models import CustomUser

class CustomUserCreationFormTestCase(TestCase):

    def test_valid_form(self):
        form_data = {
            'email': 'testuser@aluno.unb.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_domain(self):
        form_data = {
            'email': 'testuser@gmail.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Por favor, utilize um email da UNB válido.', form.errors['email'])

    def test_existing_email(self):
        CustomUser.objects.create_user(email='testuser@aluno.unb.br', password='testpassword123')
        form_data = {
            'email': 'testuser@aluno.unb.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Email já cadastrado.', form.errors['email'])

    def test_password_mismatch(self):
        form_data = {
            'email': 'testuser@aluno.unb.br',
            'password1': 'password1',
            'password2': 'password2',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Os dois campos de senha não correspondem.', form.errors['password2'])
