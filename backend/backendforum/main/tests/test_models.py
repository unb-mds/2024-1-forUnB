from django.test import TestCase
from main.models import *
from django.utils import timezone

class ForumModelTest(TestCase):

    def setUp(self):
        self.forum = Forum.objects.create(
            title="Test Forum",
            description="This is a test forum description"
        )

    # testa se o objeto Forum é criado corretamente e se seus atributos são definidos conforme esperado.
    def test_forum_creation(self):
        self.assertIsInstance(self.forum, Forum)
        self.assertEqual(self.forum.title, "Test Forum")
        self.assertEqual(self.forum.description, "This is a test forum description")
        self.assertIsNotNone(self.forum.created_at)

    # testa o método __str__ do modelo para garantir que ele retorne o título do fórum.
    def test_str_method(self):
        self.assertEqual(str(self.forum), self.forum.title)


    # testa se o campo created_at é automaticamente preenchido com a data e hora atuais quando um objeto Forum é criado.
    def test_created_at_auto_now_add(self):
        now = timezone.now()
        self.assertTrue(now - self.forum.created_at < timezone.timedelta(seconds=1))


class AnswerModelTest(TestCase):

    def setUp(self):
        self.forum = Forum.objects.create(
            title="Test Forum",
            description="This is a test forum description"
        )
        self.answer = Answer.objects.create(
            forum=self.forum,
            text="This is a test answer text that is longer than fifty characters to test the __str__ method."
        )

    #testa se o objeto Answer é criado corretamente, se seus atributos são definidos conforme esperado e se está associado corretamente ao objeto Forum.   
    def test_answer_creation(self):
        self.assertIsInstance(self.answer, Answer)
        self.assertEqual(self.answer.forum, self.forum)
        self.assertEqual(self.answer.text, "This is a test answer text that is longer than fifty characters to test the __str__ method.")
        self.assertIsNotNone(self.answer.created_at)

    
    # testa o método __str__ do modelo para garantir que ele retorne os primeiros 50 caracteres do texto da resposta, seguidos por '...'.
    def test_str_method(self):
        self.assertEqual(str(self.answer), "This is a test answer text that is longer than fif...")

    
    # testa se o campo created_at é automaticamente preenchido com a data e hora atuais quando um objeto Answer é criado.
    def test_created_at_auto_now_add(self):
        now = timezone.now()
        self.assertTrue(now - self.answer.created_at < timezone.timedelta(seconds=1)) 
    