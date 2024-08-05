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

