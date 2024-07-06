from django.test import TestCase, Client
from django.urls import reverse
from main.models import Forum
from main.forms import ForumForm

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