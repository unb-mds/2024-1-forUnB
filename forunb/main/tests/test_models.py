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
