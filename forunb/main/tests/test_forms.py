from django.test import TestCase
from main.forms import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ForumFormTest(TestCase):

    def test_forum_form_valid_data(self):
        form = ForumForm(data={'title': 'Test Forum', 'description': 'This is a test forum.'})
        self.assertTrue(form.is_valid())  # O formulário deve ser válido com dados corretos

    def test_forum_form_no_data(self):
        form = ForumForm(data={})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido sem dados
        self.assertEqual(len(form.errors), 2)  # Devem haver erros para 'title' e 'description'
