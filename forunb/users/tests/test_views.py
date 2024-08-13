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