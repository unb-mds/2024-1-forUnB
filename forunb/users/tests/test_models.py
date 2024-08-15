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
        self.forum = Forum.objects.create(title='Test Forum') # pylint: disable=E1101
        self.question = Question.objects.create( # pylint: disable=E1101
            title='Test Question',
            description='Test Description',
            author=self.user,
            forum=self.forum
        )
        self.answer = Answer.objects.create( # pylint: disable=E1101
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

        self.question.toggle_upvote(self.user)
        self.assertNotIn(self.user, self.question.upvoters.all())
        self.assertEqual(self.question.upvote_count, 0)

    def test_upvote_answer(self):
        """ Test that a user can upvote an answer """
        self.answer.toggle_upvote(self.user)
        self.assertIn(self.user, self.answer.upvoters.all())
        self.assertEqual(self.answer.upvote_count, 1)

        self.answer.toggle_upvote(self.user)
        self.assertNotIn(self.user, self.answer.upvoters.all())
        self.assertEqual(self.answer.upvote_count, 0)

    def test_notification_creation(self):
        """ Test that a notification can be created """
        notification = Notification.objects.create( # pylint: disable=E1101
            user=self.user, answer=self.answer, question=self.question
        )
        self.assertEqual(str(
            notification),
            f'Notification for {self.user.username} about question {self.question.title}')

    def test_report_creation_for_question(self):
        """ Test that a report can be created for a question """
        report = Report.objects.create( # pylint: disable=E1101
            question=self.question, user=self.user, reason='ofensivo', details='Offensive content'
        )
        self.assertEqual(
            str(report), f"Conteúdo ofensivo - {self.user.username} - Question")

    def test_report_creation_for_answer(self):
        """ Test that a report can be created for an answer """
        report = Report.objects.create( # pylint: disable=E1101
            answer=self.answer, user=self.user, reason='irrelevante', details='Irrelevant content'
        )
        self.assertEqual(
            str(report), f"Irrelevante para o fórum - {self.user.username} - Answer")
        