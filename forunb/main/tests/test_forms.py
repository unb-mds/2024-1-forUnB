from django.test import TestCase
from main.forms import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ForumFormTest(TestCase):

    def test_forum_form_valid_data(self):
        form = ForumForm(data={'title': 'Test Forum', 'description': 'This is a test forum.'})
        self.assertTrue(form.is_valid())  # O formulário deve ser válido com dados corretos

    # REMOVENDO ESTE TESTE POIS O WEBSCRAPING NAO ESTA COLETANDO DESCRICAO

    # def test_forum_form_no_data(self):
    #     form = ForumForm(data={})
    #     self.assertFalse(form.is_valid())  # O formulário não deve ser válido sem dados
    #     self.assertEqual(len(form.errors), 2)  # Devem haver erros para 'title' e 'description'



class QuestionFormTest(TestCase):

    def test_question_form_valid_data(self):
        form = QuestionForm(data={'title': 'Test Question', 'description': 'This is a test question.'})
        self.assertTrue(form.is_valid())  # O formulário deve ser válido com dados corretos

    def test_question_form_missing_title(self):
        form = QuestionForm(data={'description': 'This is a test question without a title.'})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido sem o título
        self.assertIn('title', form.errors)  # Deve haver erro para o campo 'title'



class AnswerFormTest(TestCase):

    def test_answer_form_valid_data(self):
        form = AnswerForm(data={'text': 'This is a test answer.'})
        self.assertTrue(form.is_valid())  # O formulário deve ser válido com dados corretos

    def test_answer_form_missing_text(self):
        form = AnswerForm(data={})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido sem texto
        self.assertIn('text', form.errors)  # Deve haver erro para o campo 'text'



class UnbEmailRegistrationFormTest(TestCase):

    def test_unb_email_form_valid_data(self):
        form = UnbEmailRegistrationForm(data={'email': 'student@aluno.unb.br', 'password': 'password123'})
        self.assertTrue(form.is_valid())  # O formulário deve ser válido com um e-mail UNB válido

    def test_unb_email_form_invalid_email(self):
        form = UnbEmailRegistrationForm(data={'email': 'student@example.com', 'password': 'password123'})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido com um e-mail não-UNB
        self.assertIn('email', form.errors)  # Deve haver erro para o campo 'email'

    def test_unb_email_form_existing_email(self):
        User.objects.create_user(username='testuser', email='existing@aluno.unb.br', password='password123')
        form = UnbEmailRegistrationForm(data={'email': 'existing@aluno.unb.br', 'password': 'password123'})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido se o e-mail já estiver em uso
        self.assertIn('email', form.errors)  # Deve haver erro para o campo 'email'

    def test_unb_email_form_missing_password(self):
        form = UnbEmailRegistrationForm(data={'email': 'student@aluno.unb.br'})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido sem uma senha
        self.assertIn('password', form.errors)  # Deve haver erro para o campo 'password'