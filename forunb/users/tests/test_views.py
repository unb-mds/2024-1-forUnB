from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..forms import CustomUserCreationForm
from ..models import CustomUser


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='testuser@aluno.unb.br',
            password='testpassword123',
        )

    def test_register_view_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register_unb_email.html')

    def test_register_view_post_valid(self):
        form_data = {
            'email': 'newuser@aluno.unb.br',
            'password1': 'newuserpassword123',
            'password2': 'newuserpassword123'
        }
        response = self.client.post(reverse('users:register'), form_data)
        # Should redirect to main:index
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(
            email='newuser@aluno.unb.br').exists())

    def test_register_view_post_invalid(self):
        form_data = {
            'email': 'newuser@aluno.unb.br',
            'password1': 'newuserpassword123',
            'password2': 'differentpassword123'
        }
        response = self.client.post(reverse('users:register'), form_data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(CustomUser.objects.filter(
            email='newuser@aluno.unb.br').exists())
        
    def test_logout_view(self):
        self.client.login(email=self.user.email, password='testpassword123')
        response = self.client.get(reverse('users:logout'))
        # Should redirect to main:index
        self.assertEqual(response.status_code, 302)

    def test_login_view_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('users:login'), {
            'username': self.user.email,
            'password': 'testpassword123'
        })
        # Should redirect to main:index
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_invalid_email(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'nonexistent@aluno.unb.br',
            'password': 'somepassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username',
                             "Este email não está cadastrado.")
        
    def test_login_view_post_invalid_password(self):
        response = self.client.post(reverse('users:login'), {
            'username': self.user.email,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', "Senha incorreta.")