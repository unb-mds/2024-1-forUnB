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

    def test_create_superuser(self):
        """ Test that a superuser can be created """
        admin_user = CustomUser.objects.create_superuser(
            email='admin@aluno.unb.br', password='adminpass'
        )
        self.assertEqual(admin_user.email, 'admin@aluno.unb.br')
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_str_method(self):
        """ Test that the __str__ method returns the username """
        self.assertEqual(str(self.user), self.user.username)

    def test_upvote_question(self):
        """ Test that a user can upvote a question """
        self.question.toggle_upvote(self.user)
        self.assertIn(self.user, self.question.upvoters.all())
        self.assertEqual(self.question.upvote_count, 1)