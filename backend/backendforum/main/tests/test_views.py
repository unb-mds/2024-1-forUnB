from django.test import TestCase, Client
from django.urls import reverse
from main.models import *
from main.forms import *

class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    # testa se a view index retorna um código de status HTTP 200, indicando que a página foi carregada com sucesso.
    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    
    # testa se a view index usa o template correto, 'main/index.html'.
    def test_index_view_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'main/index.html')



class NewQuestionViewTest(TestCase):

    def setUp(self):
        self.client = Client()


    # Testa a resposta a uma solicitação GET para a view new_question:
    #   - Verifica se o código de status da resposta é 200 (OK).
    #   - Verifica se o template correto (main/new_question.html) é usado.
    #   - Verifica se o contexto da resposta contém um formulário ForumForm.
    def test_new_question_view_get(self):
        response = self.client.get(reverse('new_question'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/new_question.html')
        self.assertIsInstance(response.context['form'], ForumForm)


    # Testa a resposta a uma solicitação POST com dados válidos:
    #   - Envia uma solicitação POST para a URL new_question com dados válidos.
    #   - Verifica se o código de status da resposta é 302 (redirecionamento após o envio bem-sucedido).
    #   - Verifica se a resposta redireciona para a URL questions.
    #   - Verifica se um objeto Forum foi criado no banco de dados com os dados corretos.
    def test_new_question_view_post_valid_data(self):
        data = {
            'title': 'Test Question',
            'description': 'This is a test question description.'
        }
        response = self.client.post(reverse('new_question'), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após o sucesso
        self.assertRedirects(response, reverse('questions'))
        self.assertEqual(Forum.objects.count(), 1)
        new_question = Forum.objects.first()
        self.assertEqual(new_question.title, 'Test Question')
        self.assertEqual(new_question.description, 'This is a test question description.')

    
    # testa a resposta a uma solicitação POST com dados inválidos:
    #   - Envia uma solicitação POST para a URL new_question com dados inválidos (título vazio).
    #   - Verifica se o código de status da resposta é 200 (o formulário é reapresentado com erros).
    #   - Verifica se o template correto (main/new_question.html) é usado.
    #   - Verifica se o contexto da resposta contém um formulário ForumForm com erros.
    #   - Verifica se nenhum objeto Forum foi criado no banco de dados.
    def test_new_question_view_post_invalid_data(self):
        data = {
            'title': '',  # Título vazio para invalidar o formulário
            'description': 'This is a test question description.'
        }
        response = self.client.post(reverse('new_question'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/new_question.html')
        self.assertIsInstance(response.context['form'], ForumForm)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Forum.objects.count(), 0)


class QuestionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.forum = Forum.objects.create(
            title="Test Question",
            description="This is a test question description."
        )

    # testa a resposta a uma solicitação GET para a view question:
    #   - Verifica se o código de status da resposta é 200 (OK).
    #   - Verifica se o template correto (main/question.html) é usado.
    #   - Verifica se a resposta contém o título e a descrição da pergunta.
    #   - Verifica se o contexto da resposta contém o objeto Forum correto.
    def test_question_view(self):
        response = self.client.get(reverse('question', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/question.html')
        self.assertContains(response, self.forum.title)
        self.assertContains(response, self.forum.description)
        self.assertEqual(response.context['question'], self.forum)


class QuestionsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.forum1 = Forum.objects.create(
            title="Test Question 1",
            description="This is a test question description 1."
        )
        self.forum2 = Forum.objects.create(
            title="Test Question 2",
            description="This is a test question description 2."
        )

    # Testa a resposta a uma solicitação GET para a view questions:
    #   - Verifica se o código de status da resposta é 200 (OK).
    #   - Verifica se o template correto (main/questions.html) é usado.
    #   - Verifica se a resposta contém os títulos e descrições das perguntas.
    #   - Verifica se o contexto da resposta contém a lista de perguntas correta.
    def test_questions_view_status_code(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, 200)

    def test_questions_view_template_used(self):
        response = self.client.get(reverse('questions'))
        self.assertTemplateUsed(response, 'main/questions.html')

    def test_questions_view_context(self):
        response = self.client.get(reverse('questions'))
        self.assertIn(self.forum1, response.context['questions'])
        self.assertIn(self.forum2, response.context['questions'])

    def test_questions_view_content(self):
        response = self.client.get(reverse('questions'))
        self.assertContains(response, self.forum1.title)
        self.assertContains(response, self.forum2.title)


class NewAnswerViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.forum = Forum.objects.create(
            title="Test Question",
            description="This is a test question description."
        )

    # Testa a resposta a uma solicitação GET para a view new_answer:
    #   - Verifica se o código de status da resposta é 200 (OK).
    #   - Verifica se o template correto (main/new_answer.html) é usado.
    #   - Verifica se o contexto da resposta contém um formulário AnswerForm.
    #   - Verifica se o contexto da resposta contém o objeto Forum correto.
    def test_new_answer_view_get(self):
        response = self.client.get(reverse('new_answer', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/new_answer.html')
        self.assertIsInstance(response.context['form'], AnswerForm)
        self.assertEqual(response.context['question'], self.forum)

    # Testa a resposta a uma solicitação POST com dados válidos:
    #   - Envia uma solicitação POST para a URL new_answer com dados válidos.
    #   - Verifica se o código de status da resposta é 302 (redirecionamento após o envio bem-sucedido).
    #   - Verifica se a resposta redireciona para a URL da pergunta.
    #   - Verifica se um objeto Answer foi criado no banco de dados com os dados corretos.
    def test_new_answer_view_post_valid_data(self):
        data = {
            'text': 'This is a test answer.'
        }
        response = self.client.post(reverse('new_answer', args=[self.forum.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após o sucesso
        self.assertRedirects(response, reverse('question', args=[self.forum.id]))
        self.assertEqual(Answer.objects.count(), 1)
        new_answer = Answer.objects.first()
        self.assertEqual(new_answer.text, 'This is a test answer.')
        self.assertEqual(new_answer.forum, self.forum)

    # Testa a resposta a uma solicitação POST com dados inválidos:
    #   - Envia uma solicitação POST para a URL new_answer com dados inválidos (texto vazio).
    #   - Verifica se o código de status da resposta é 200 (o formulário é reapresentado com erros).
    #   - Verifica se o template correto (main/new_answer.html) é usado.
    #   - Verifica se o contexto da resposta contém um formulário AnswerForm com erros.
    #   - Verifica se nenhum objeto Answer foi criado no banco de dados.
    def test_new_answer_view_post_invalid_data(self):
        data = {
            'text': ''  # Texto vazio para invalidar o formulário
        }
        response = self.client.post(reverse('new_answer', args=[self.forum.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/new_answer.html')
        self.assertIsInstance(response.context['form'], AnswerForm)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Answer.objects.count(), 0)
