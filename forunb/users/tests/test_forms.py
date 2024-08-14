"""Tests for forms in the users application."""

from django.test import TestCase
from ..forms import CustomUserCreationForm, CustomUserChangeForm
from ..models import CustomUser


class CustomUserCreationFormTestCase(TestCase):
    """Test cases for the CustomUserCreationForm."""

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        form_data = {
            'email': 'testuser@aluno.unb.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_domain(self):
        """Test that the form is invalid with a non-UnB email domain."""
        form_data = {
            'email': 'testuser@gmail.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Por favor, utilize um email da UnB válido.', form.errors['email'])

    def test_existing_email(self):
        """Test that the form is invalid if the email already exists."""
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
        """Test that the form is invalid if the passwords do not match."""
        form_data = {
            'email': 'testuser@aluno.unb.br',
            'password1': 'password1',
            'password2': 'password2',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Os dois campos de senha não correspondem.', form.errors['password2'])

    def test_save_form(self):
        """Test that the form saves a valid user correctly."""
        form_data = {
            'email': 'testuser@aluno.unb.br',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        user = form.save()
        self.assertEqual(user.email, 'testuser@aluno.unb.br')
        self.assertTrue(user.check_password('testpassword123'))


class CustomUserChangeFormTestCase(TestCase):
    """Test cases for the CustomUserChangeForm."""

    def setUp(self):
        """Set up a user instance for testing."""
        self.user = CustomUser.objects.create_user(
            email='testuser@aluno.unb.br',
            password='testpassword123',
        )

    def test_valid_change_form(self):
        """Test that the change form is valid with correct data."""
        form_data = {
            'email': self.user.email,
            'username': 'newusername',
        }
        form = CustomUserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'newusername')


class ProfileEditFormTestCase(TestCase):
    """Test cases for the ProfileEditForm."""

    def setUp(self):
        """Set up a user instance for testing the profile edit form."""
        self.user = CustomUser.objects.create_user(
            email='testuser@aluno.unb.br',
            password='testpassword123',
            username='testuser'
        )

    # O teste abaixo foi comentado, precisa ser corrigido.
    # def test_valid_profile_edit_form(self):
    #     """Test that the profile edit form is valid with correct data."""
    #     form_data = {
    #         'username': 'newusername',
    #     }
    #     form = ProfileEditForm(data=form_data, instance=self.user)
    #     self.assertTrue(form.is_valid())
    #     user = form.save()
    #     self.assertEqual(user.username, 'newusername')

    # O teste abaixo foi comentado, precisa ser corrigido.
    # def test_invalid_username_taken(self):
    #     """Test that the profile edit form is invalid if the username is already taken."""
    #     CustomUser.objects.create_user
    #    (email='otheruser@aluno.unb.br', password='password123', username='newusername')
    #     form_data = {
    #         'username': 'newusername',
    #     }
    #     form = ProfileEditForm(data=form_data, instance=self.user)
    #     self.assertFalse(form.is_valid())
    #     self.assertIn("Este nome de usuário já está em uso.", form.errors['username'])
