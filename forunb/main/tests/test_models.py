from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from main.models import Forum, Question, Answer

User = get_user_model()

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

    def test_forum_title_max_length(self):
        max_length = self.forum._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)  # Verifica se o tamanho máximo do título é 100

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@aluno.unb.br', password='senha1010')
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

    def test_question_title_max_length(self):
        max_length = self.question._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)  # Verifica se o tamanho máximo do título é 100

    '''def test_question_missing_title(self):
        question = Question(description='Test Description', author=self.user, forum=self.forum)
        with self.assertRaises(ValidationError) as context:  # Verifica se ocorre erro ao criar uma pergunta sem título
            question.full_clean()
        self.assertTrue('title' in context.exception.message_dict)  # Verifica se o erro de validação está relacionado ao campo 'title' '''

class AnswerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@aluno.unb.br', password='senha1010')
        cls.forum = Forum.objects.create(title='Test Forum', description='Test Description')
        cls.question = Question.objects.create(
            title='Test Question',
            description='Test Description',
            author=cls.user,
            forum=cls.forum
        )
        cls.answer = Answer.objects.create(
            text='Test Answer',
            author=cls.user,
            question=cls.question
        )

    def test_answer_creation(self):
        self.assertIsInstance(self.answer, Answer)  # Verifica se o objeto é uma instância de Answer
        self.assertEqual(self.answer.text, 'Test Answer')  # Verifica se o texto da resposta é 'Test Answer'
        self.assertEqual(self.answer.author, self.user)  # Verifica se o autor da resposta é o usuário de teste
        self.assertEqual(self.answer.question, self.question)  # Verifica se a pergunta associada é a pergunta de teste
        self.assertTrue(hasattr(self.answer, 'created_at'))  # Verifica se o atributo 'created_at' existe
        self.assertEqual(self.answer.upvoters.count(), 0)  # Verifica se o número de upvotes é 0

    def test_answer_str_method(self):
        self.assertEqual(str(self.answer), 'Test Answer...')  # Verifica se o método __str__ retorna o início do texto da resposta

    def test_answer_missing_text(self):
        answer = Answer(author=self.user, question=self.question)
        with self.assertRaises(ValidationError):  # Verifica se ocorre erro ao criar uma resposta sem texto
            answer.full_clean()

    def test_delete_question_deletes_answers(self):
        question_id = self.question.id
        self.question.delete()
        with self.assertRaises(Answer.DoesNotExist):  # Verifica se as respostas associadas são deletadas junto com a pergunta
            Answer.objects.get(question__id=question_id)
