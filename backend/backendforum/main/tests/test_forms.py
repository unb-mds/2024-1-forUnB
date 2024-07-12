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


class AnswerFormTest(TestCase):

    # Testa com Dados Válidos
    def test_answer_form_valid_data(self):
        form_data = {
            'text': 'This is a valid answer.'
        }
        form = AnswerForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Testa com Dados Vazios 
    def test_answer_form_empty_data(self):
        form_data = {}
        form = AnswerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Verifica se há 1 erro (para o campo 'text')

    # Testa com Texto Ausente
    def test_answer_form_missing_text(self):
        form_data = {}
        form = AnswerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors.keys())  # Verifica se há um erro relacionado ao campo 'text'
"""
    # Testa com Texto muito curto
    def test_answer_form_text_too_short(self):
        form_data = {
            'text': 'Short'
        }
        form = AnswerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors.keys())  # Verifica se há um erro relacionado ao campo 'text'
        """