from django.test import TestCase
from main.forms import *
from users.forms import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ForumFormTest(TestCase):

    def test_forum_form_valid_data(self):
        form = ForumForm(data={'title': 'Test Forum', 'description': 'This is a test forum.'})
        self.assertTrue(form.is_valid())  # O formulário deve ser válido com dados corretos

    def test_forum_form_no_data(self):
        form = ForumForm(data={})
        self.assertFalse(form.is_valid())  # O formulário não deve ser válido sem dados
        self.assertIn('title', form.errors)  # Deve haver erro para o campo 'title'



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


from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser

class CustomUserFormTests(TestCase):

    def test_invalid_unb_email(self):
        """Testa se o formulário rejeita um email que não é da UNB."""
        form_data = {'email': 'invalid@example.com', 'password1': 'password', 'password2': 'password'}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_valid_unb_email(self):
        """Testa se o formulário aceita um email válido da UNB."""
        form_data = {'email': 'valid@aluno.unb.br', 'password1': 'password1010', 'password2': 'password1010'}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_user(self):
        """Testa se o formulário cria um usuário com sucesso."""
        form_data = {'email': 'valid@aluno.unb.br', 'password1': 'password1010', 'password2': 'password1010'}
        form = CustomUserCreationForm(data=form_data)
        if form.is_valid():
            user = form.save(commit=False)
            self.assertEqual(user.email, 'valid@aluno.unb.br')
            self.assertEqual(user.username, 'valid@aluno.unb.br')
            user.save()
            self.assertEqual(CustomUser.objects.count(), 1)
        else:
            self.fail(form.errors)

    def test_change_user(self):
        #Testa se o formulário de mudança de usuário permite atualizações.
            
        # Criar usuário inicial
        user = CustomUser.objects.create_user(email='valid@aluno.unb.br', password='password')
        
        # Dados para atualização
        form_data = {
            'email': 'valid@aluno.unb.br',  # O email deve permanecer o mesmo para passar pela validação
            'username': 'newusername',  # Novo nome de usuário
            'is_active': True,  # Atualizando estado de atividade
            'is_staff': False  # Atualizando permissão de staff
        }
        
        # Formulário de mudança com os novos dados
        form = CustomUserChangeForm(data=form_data, instance=user)
        
        # Verificando se o formulário é válido
        self.assertTrue(form.is_valid(), form.errors)  # Incluindo form.errors para debug
        updated_user = form.save(commit=False)
        self.assertEqual(updated_user.username, 'newusername')
        updated_user.save()
        
        # Verificando se a atualização foi aplicada
        user.refresh_from_db()  # Recarregar do banco de dados
        self.assertEqual(user.username, 'newusername')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)


