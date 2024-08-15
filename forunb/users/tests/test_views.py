"""Tests for the views in the users application."""

from django.test import TestCase, Client
from django.urls import reverse
from ..models import CustomUser


class UserViewsTestCase(TestCase):
    """Test cases for the user-related views."""

    def setUp(self):
        """Set up the client and a test user."""
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='testuser@aluno.unb.br',
            password='testpassword123',
        )

    def test_register_view_get(self):
        """Test GET request to the register view."""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register_unb_email.html')

    def test_register_view_post_valid(self):
        """Test POST request with valid data to the register view."""
        form_data = {
            'email': 'newuser@aluno.unb.br',
            'password1': 'newuserpassword123',
            'password2': 'newuserpassword123'
        }
        response = self.client.post(reverse('users:register'), form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect to main:index
        self.assertTrue(CustomUser.objects.filter(email='newuser@aluno.unb.br').exists())

    def test_register_view_post_invalid(self):
        """Test POST request with invalid data to the register view."""
        form_data = {
            'email': 'newuser@aluno.unb.br',
            'password1': 'newuserpassword123',
            'password2': 'differentpassword123'
        }
        response = self.client.post(reverse('users:register'), form_data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(CustomUser.objects.filter(email='newuser@aluno.unb.br').exists())

    def test_logout_view(self):
        """Test GET request to the logout view."""
        self.client.login(email=self.user.email, password='testpassword123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect to main:index

    def test_login_view_get(self):
        """Test GET request to the login view."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_valid(self):
        """Test POST request with valid credentials to the login view."""
        response = self.client.post(reverse('users:login'), {
            'username': self.user.email,
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to main:index

    def test_login_view_post_invalid_email(self):
        """Test POST request with an invalid email to the login view."""
        response = self.client.post(reverse('users:login'), {
            'username': 'nonexistent@aluno.unb.br',
            'password': 'somepassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "Este email não está cadastrado.")

    def test_login_view_post_invalid_password(self):
        """Test POST request with an invalid password to the login view."""
        response = self.client.post(reverse('users:login'), {
            'username': self.user.email,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', "Senha incorreta.")

    def test_profile_view(self):
        """Test GET request to the profile view."""
        self.client.login(email=self.user.email, password='testpassword123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_view_post_valid(self):
        """Test POST request with valid data to the edit profile view."""
        self.client.login(email=self.user.email, password='testpassword123')
        response = self.client.post(reverse('users:edit_profile'), {
            'username': 'newusername',
            'photo': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

    # O teste abaixo foi comentado, precisa ser corrigido.
    # def test_edit_profile_view_post_invalid(self):
    #     """Test POST request with invalid data to the edit profile view."""
    #     self.client.login(email=self.user.email, password='testpassword123')
    #     CustomUser.objects.create_user(
    #         email='anotheruser@aluno.unb.br', password='anotherpassword123')
    #     response = self.client.post(reverse('users:edit_profile'), {
    #         'username': 'existingusername',
    #         'photo': '',
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(response.content, {
    #                          'success': False, 'errors': 'Este nome de usuário já está em uso.'})

    # O teste abaixo foi comentado, precisa ser corrigido.
    # def test_edit_profile_view_get(self):
    #     """Test that GET request to edit profile view is not allowed."""
    #     self.client.login(email=self.user.email, password='testpassword123')
    #     response = self.client.get(reverse('users:edit_profile'))
    #     # Method not allowed for GET requests
    #     self.assertEqual(response.status_code, 405)
