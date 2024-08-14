"""Tests for the URL configurations in the users application."""

from django.test import TestCase
from django.urls import reverse, resolve
from ..views import register, logout_view, login_view


class UsersURLTests(TestCase):
    """Test cases for the URLs in the users app."""

    def test_register_url(self):
        """Test that the register URL resolves to the correct view."""
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, register)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        """Test that the logout URL resolves to the correct view."""
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, logout_view)
        response = self.client.get(url)
        # Since logout redirects, we check for status code 302
        self.assertEqual(response.status_code, 302)

    def test_login_url(self):
        """Test that the login URL resolves to the correct view."""
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, login_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        """Test that the edit profile URL requires login."""
        url = reverse('users:edit_profile')
        response = self.client.get(url)
        # Since the user is not logged in, the status code should be 302
        self.assertEqual(response.status_code, 302)
