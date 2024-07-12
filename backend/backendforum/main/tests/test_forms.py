from django.test import TestCase
from main.forms import *

class ForumFormTest(TestCase):

    # Testa com Dados Válidos
    def test_forum_form_valid_data(self):
        form_data = {
            'title': 'Test Question',
            'description': 'This is a test question description.'
        }
        form = ForumForm(data=form_data)
        self.assertTrue(form.is_valid())


    # Testa com Dados Vazios 
    def test_forum_form_empty_data(self):
        form_data = {}
        form = ForumForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Verifica se há 2 erros (um para cada campo obrigatório)

    # Testa com Título Ausente
    def test_forum_form_missing_title(self):
        form_data = {
            'description': 'This is a test question description.'
        }
        form = ForumForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())  # Verifica se há um erro relacionado ao campo 'title'


    # Testa com Descrição Ausente
    def test_forum_form_missing_description(self):
        form_data = {
            'title': 'Test Question'
        }
        form = ForumForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())


