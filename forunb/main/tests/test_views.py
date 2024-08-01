from django.test import TestCase, Client
from django.urls import reverse
from main.models import Forum, Question, Answer
from django.contrib.auth import get_user_model

User = get_user_model()

class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'main/index.html')

class ViewsTestCase(TestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(email='test@aluno.unb.br', password='senha1010')

        # Create a Forum
        self.forum = Forum.objects.create(title="Test Forum", description="Test Forum Description")

        # Create a Question
        self.question = Question.objects.create(title="Test Question", description="Test Question Description", forum=self.forum, author=self.user)

        # Create an Answer
        self.answer = Answer.objects.create(text="Test Answer", question=self.question, author=self.user)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, self.question.title)

    def test_forum_detail_view(self):
        response = self.client.get(reverse('forum_detail', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forum_detail.html')
        self.assertContains(response, self.forum.title)

    def test_forum_list_view(self):
        response = self.client.get(reverse('forum_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forums.html')
        self.assertContains(response, self.forum.title)

    def test_questions_view(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/questions.html')
        self.assertContains(response, self.question.title)

    def test_question_detail_view(self):
        response = self.client.get(reverse('question_detail', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/question_detail.html')
        self.assertContains(response, self.question.title)

    def test_new_question_view(self):
        self.client.login(email='test@aluno.unb.br', password='senha1010')
        response = self.client.get(reverse('new_question', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/new_question.html')

        # Test posting a new question
        response = self.client.post(reverse('new_question', args=[self.forum.id]), {
            'title': 'Another Test Question',
            'description': 'Another Test Question Description',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_new_answer_view(self):
        self.client.login(email='test@aluno.unb.br', password='senha1010')
        response = self.client.get(reverse('new_answer', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/new_answer.html')

        # Test posting a new answer
        response = self.client.post(reverse('new_answer', args=[self.question.id]), {
            'text': 'Another Test Answer',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success


# TESTANDO VIEWS DO APP SEARCH

class SearchForumTestCase(TestCase):

    def setUp(self):
        # Configuração inicial para criar alguns objetos de fórum
        self.client = Client()
        self.forum1 = Forum.objects.create(title="Python Programming", description="Discuss all things Python.")
        self.forum2 = Forum.objects.create(title="Django Tips", description="Tips and tricks for Django.")
        self.forum3 = Forum.objects.create(title="Web Development", description="General web development discussion.")

    def test_search_forum_with_query(self):
        # Envia uma solicitação GET com um parâmetro de pesquisa
        response = self.client.get(reverse('search_forum') + '?search=python')
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'main/forums.html')
        
        # Verifica se o contexto contém os fóruns filtrados
        self.assertIn('forums', response.context)
        forums = response.context['forums']
        self.assertEqual(forums.count(), 1)
        self.assertEqual(forums[0], self.forum1)
        
        # Verifica se a consulta de pesquisa foi passada corretamente para o contexto
        self.assertEqual(response.context['query'], 'python')

    def test_search_forum_with_no_results(self):
        # Envia uma solicitação GET com um parâmetro de pesquisa que não deve retornar resultados
        response = self.client.get(reverse('search_forum') + '?search=java')
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'main/forums.html')
        
        # Verifica se o contexto contém a lista de fóruns vazia
        self.assertIn('forums', response.context)
        forums = response.context['forums']
        self.assertEqual(forums.count(), 0)
        
        # Verifica se a consulta de pesquisa foi passada corretamente para o contexto
        self.assertEqual(response.context['query'], 'java')
