from django.test import TestCase
from django.urls import reverse, resolve
from ..views import register, Logout_view, login_view


class UsersURLTests(TestCase):
    """ Testes da URL do app users. """

    def test_register_url(self):
        """ Testa se a URL de registro está correta. """
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, register)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        """ Testa se a URL de logout está correta. """
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, Logout_view)
        response = self.client.get(url)
        # Como o logout redireciona, verificamos o código de status 302
        self.assertEqual(response.status_code, 302)

    def test_login_url(self):
        """ Testa se a URL de login está correta. """
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, login_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        """ Testa se a URL de edição de perfil está correta. """
        url = reverse('users:edit_profile')
        response = self.client.get(url)
        # Como o usuário não está logado, o código de status deve ser 302
        self.assertEqual(response.status_code, 302) 