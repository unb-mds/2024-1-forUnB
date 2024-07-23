from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Question, Answer, Forum

class ForumModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.forum = Forum.objects.create(title='Test Forum', description='Test Description')

    def test_forum_creation(self):
        self.assertIsInstance(self.forum, Forum)  # Verifica se o objeto é uma instância de Forum
        self.assertEqual(self.forum.title, 'Test Forum')  # Verifica se o título do fórum é 'Test Forum'
        self.assertEqual(self.forum.description, 'Test Description')  # Verifica se a descrição do fórum é 'Test Description'
        self.assertTrue(hasattr(self.forum, 'created_at'))  # Verifica se o atributo 'created_at' existe

    def test_forum_str_method(self):
        self.assertEqual(str(self.forum), 'Test Forum')  # Verifica se o método __str__ retorna o título do fórum


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.forum = Forum.objects.create(title='Test Forum', description='Test Description')
        cls.question = Question.objects.create(
            title='Test Question',
            description='Test Description',
            author=cls.user,
            forum=cls.forum
        )

    def test_question_creation(self):
        self.assertIsInstance(self.question, Question)  # Verifica se o objeto é uma instância de Question
        self.assertEqual(self.question.title, 'Test Question')  # Verifica se o título da pergunta é 'Test Question'
        self.assertEqual(self.question.description, 'Test Description')  # Verifica se a descrição da pergunta é 'Test Description'
        self.assertEqual(self.question.author, self.user)  # Verifica se o autor da pergunta é o usuário de teste
        self.assertEqual(self.question.forum, self.forum)  # Verifica se o fórum associado é o fórum de teste
        self.assertTrue(hasattr(self.question, 'created_at'))  # Verifica se o atributo 'created_at' existe
        self.assertEqual(self.question.favoritados, 0)  # Verifica se o número de favoritos é 0

    def test_question_str_method(self):
        self.assertEqual(str(self.question), 'Test Question')  # Verifica se o método __str__ retorna o título da pergunta
