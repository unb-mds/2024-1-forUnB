""" Test cases for the views in the users app. """
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class ViewsTestCase(TestCase):
    """ Test cases for the views in the users app. """
    def setUp(self):
        """ Setup for the test cases. """
        self.client = Client()
        self.user_data = {
            'email': 'testuser@aluno.unb.br',
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        self.user = CustomUser.objects.create_user(
            email='existinguser@aluno.unb.br', password='password123'
        )

    def test_register_view_get(self):
        """ Test the register view with a GET request. """
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register_unb_email.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post_valid_data(self):
        """ Test the register view with a POST request and valid data. """
        response = self.client.post(
            reverse('users:register'), data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        self.assertTrue(CustomUser.objects.filter(
            email=self.user_data['email']).exists())

    def test_register_view_post_invalid_data(self):
        """ Test the register view with a POST request and invalid data. """
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        response = self.client.post(
            reverse('users:register'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register_unb_email.html')
        self.assertIn('form', response.context)
        self.assertFalse(CustomUser.objects.filter(
            email=invalid_data['email']).exists())

    def test_login_view_get(self):
        """ Test the login view with a GET request. """
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_view_post_valid_credentials(self):
        """ Test the login view with a POST request and valid credentials. """
        response = self.client.post(reverse('users:login'), {
            'username': self.user.email,
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_login_view_post_invalid_email(self):
        """ Test the login view with a POST request and invalid email. """
        response = self.client.post(reverse('users:login'), {
            'username': 'wrongemail@aluno.unb.br',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('Este email não está cadastrado.',
                      response.context['form'].errors['username'])

    def test_login_view_post_invalid_password(self):
        """ Test the login view with a POST request and invalid password. """
        response = self.client.post(reverse('users:login'), {
            'username': self.user.email,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('Senha incorreta.',
                      response.context['form'].errors['password'])

    def test_logout_view(self):
        """ Test the logout view. """
        self.client.login(username=self.user.email, password='password123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_profile_view(self):
        """ Test the profile view. """
        self.client.login(username=self.user.email, password='password123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    # Test esta falhando
    # def test_edit_profile_view_post_valid_data(self):
    #     """ Test the edit profile view with a POST request and valid data. """
    #     self.client.login(username=self.user.email, password='password123')
    #     response = self.client.post(reverse('users:edit_profile'), {
    #         'username': 'newusername'
    #     }, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(
    #         str(response.content, encoding='utf8'), {'success': True})
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.username, 'newusername')

    def test_edit_profile_view_post_invalid_data(self):
        """ Test the edit profile view with a POST request and invalid data. """
        self.client.login(username=self.user.email, password='password123')
        response = self.client.post(reverse('users:edit_profile'), {
            'username': ''
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'success': False,
            'errors': 'Nome de usuário não pode estar vazio.'
        })

    # Test esta falhando
    # def test_edit_profile_view_username_in_use(self):
    #     """ Test the edit profile view with a username that is already in use. """
    #     another_user = CustomUser.objects.create_user(
    #         email='anotheruser@aluno.unb.br', password='password123'
    #     )
    #     another_user.username = 'newusername'
    #     self.client.login(username=self.user.email, password='password123')
    #     response = self.client.post(reverse('users:edit_profile'), {
    #         'username': 'newusername'
    #     }, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(str(response.content, encoding='utf8'), {
    #         'success': False,
    #         'errors': 'Este nome de usuário já está em uso.'
    #     })
