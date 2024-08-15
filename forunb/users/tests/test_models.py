""" Tests for the CustomUser model """
from django.test import TestCase
from users.models import CustomUser
from main.models import Forum, Question, Answer, Notification, Report


class CustomUserModelTest(TestCase):
    """ Test cases for the CustomUser model """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@aluno.unb.br', password='password123'
        )
        self.forum = Forum.objects.create(title='Test Forum')
        self.question = Question.objects.create(
            title='Test Question',
            description='Test Description',
            author=self.user,
            forum=self.forum
        )
        self.answer = Answer.objects.create(
            question=self.question, text='Test Answer', author=self.user
        )

    def test_create_user(self):
        """ Test that a user can be created """
        self.assertEqual(self.user.email, 'testuser@aluno.unb.br')
        self.assertTrue(self.user.check_password('password123'))
        self.assertFalse(self.user.is_staff)

    