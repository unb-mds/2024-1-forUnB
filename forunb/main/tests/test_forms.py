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

class QuestionFormTest(TestCase):

    def test_question_form_valid_data(self):
        form = QuestionForm(data={'title': 'Test Question', 'description': 'This is a test question.'})
        self.assertTrue(form.is_valid())  # O formulário deve ser válido com dados corretos

    def test_question_form_missing_title(self):
        form = QuestionForm(data={'description': 'This is a test question without a title.'})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido sem o título
        self.assertIn('title', form.errors)  # Deve haver erro para o campo 'title'