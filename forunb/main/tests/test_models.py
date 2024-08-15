"""Test suite for the models of the main app."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from main.models import Forum, Question, Answer, Notification, Report

User = get_user_model()


class ForumModelTest(TestCase):
    """ Test suite for the Forum model."""
    @classmethod
    def setUpTestData(cls):
        cls.forum = Forum.objects.create( # pylint: disable=E1101
            title='Test Forum', description='Test Description')

    def test_forum_creation(self):
        """ Set up data for the entire TestCase."""
        self.assertIsInstance(self.forum, Forum)
        self.assertEqual(self.forum.title, 'Test Forum')
        self.assertEqual(self.forum.description, 'Test Description')
        self.assertTrue(hasattr(self.forum, 'created_at'))

    def test_forum_str_method(self):
        """ Test the __str__ method of the Forum model."""
        self.assertEqual(str(self.forum), 'Test Forum')

    def test_forum_title_max_length(self):
        """ Test the max_length of the title field. """
        max_length = self.forum._meta.get_field('title').max_length  # pylint: disable=protected-access
        self.assertEqual(max_length, 100)


class QuestionModelTest(TestCase):
    """ Test suite for the Question model. """
    @classmethod
    def setUpTestData(cls):
        """ Set up data for the entire TestCase. """
        cls.user = User.objects.create_user(
            email='test@aluno.unb.br', password='senha1010')
        cls.forum = Forum.objects.create( # pylint: disable=E1101
            title='Test Forum', description='Test Description')
        cls.question = Question.objects.create( # pylint: disable=E1101
            title='Test Question',
            description='Test Description',
            author=cls.user,
            forum=cls.forum
        )

    def test_question_creation(self):
        """ Test the creation of a Question object. """
        self.assertIsInstance(self.question, Question)
        self.assertEqual(self.question.title, 'Test Question')
        self.assertEqual(self.question.description, 'Test Description')
        self.assertEqual(self.question.author, self.user)
        self.assertEqual(self.question.forum, self.forum)
        self.assertTrue(hasattr(self.question, 'created_at'))
        self.assertEqual(self.question.favoritados, 0)

    def test_question_str_method(self):
        """ Test the __str__ method of the Question model. """
        self.assertEqual(str(self.question), 'Test Question')

    def test_question_title_max_length(self):
        """ Test the max_length of the title field. """
        max_length = self.question._meta.get_field('title').max_length  # pylint: disable=protected-access
        self.assertEqual(max_length, 100)

    def test_question_toggle_upvote(self):
        """ Test the toggle_upvote method of the Question model. """
        self.assertEqual(self.question.upvote_count, 0)
        self.question.toggle_upvote(self.user)
        self.assertEqual(self.question.upvote_count, 1)
        self.question.toggle_upvote(self.user)
        self.assertEqual(self.question.upvote_count, 0)

    # def test_question_missing_title(self):
    #     question = Question(description='Test Description', author=self.user, forum=self.forum)
    #     with self.assertRaises(ValidationError) as context:
    #         question.full_clean()
    #     self.assertTrue('title' in context.exception.message_dict)


class AnswerModelTest(TestCase):
    """ Test suite for the Answer model. """
    @classmethod
    def setUpTestData(cls):
        """ Set up data for the entire TestCase. """
        cls.user = User.objects.create_user(
            email='test@aluno.unb.br', password='senha1010')
        cls.forum = Forum.objects.create( # pylint: disable=E1101
            title='Test Forum', description='Test Description')
        cls.question = Question.objects.create( # pylint: disable=E1101
            title='Test Question',
            description='Test Description',
            author=cls.user,
            forum=cls.forum
        )
        cls.answer = Answer.objects.create( # pylint: disable=E1101
            text='Test Answer',
            author=cls.user,
            question=cls.question
        )

    def test_answer_creation(self):
        """ Test the creation of an Answer object. """
        self.assertIsInstance(self.answer, Answer)
        self.assertEqual(self.answer.text, 'Test Answer')
        self.assertEqual(self.answer.author, self.user)
        self.assertEqual(self.answer.question, self.question)
        self.assertTrue(hasattr(self.answer, 'created_at'))
        self.assertEqual(self.answer.upvoters.count(), 0)

    def test_answer_str_method(self):
        """ Test the __str__ method of the Answer model. """
        self.assertEqual(str(self.answer), 'Test Answer...')

    def test_answer_missing_text(self):
        """ Test the full_clean method of the Answer model. """
        answer = Answer(author=self.user, question=self.question)
        with self.assertRaises(ValidationError):
            answer.full_clean()

    def test_delete_question_deletes_answers(self):
        """ Test if deleting a question deletes its associated answers. """
        question_id = self.question.id
        self.question.delete()
        with self.assertRaises(Answer.DoesNotExist): # pylint: disable=E1101
            Answer.objects.get(question__id=question_id) # pylint: disable=E1101

    def test_answer_toggle_upvote(self):
        """ Test the toggle_upvote method of the Answer model. """
        self.assertEqual(self.answer.upvote_count, 0)
        self.answer.toggle_upvote(self.user)
        self.assertEqual(self.answer.upvote_count, 1)
        self.answer.toggle_upvote(self.user)
        self.assertEqual(self.answer.upvote_count, 0)


class NotificationModelTest(TestCase):
    """ Test suite for the Notification model. """
    @classmethod
    def setUpTestData(cls):
        """ Set up data for the entire TestCase. """
        cls.user = User.objects.create_user(
            email='test@aluno.unb.br', password='senha1010')
        cls.forum = Forum.objects.create( # pylint: disable=E1101
            title='Test Forum', description='Test Description')
        cls.question = Question.objects.create( # pylint: disable=E1101
            title='Test Question',
            description='Test Description',
            author=cls.user,
            forum=cls.forum
        )
        cls.answer = Answer.objects.create( # pylint: disable=E1101
            text='Test Answer',
            author=cls.user,
            question=cls.question
        )
        cls.notification = Notification.objects.create( # pylint: disable=E1101
            user=cls.user,
            question=cls.question,
            answer=cls.answer
        )

    def test_notification_creation(self):
        """ Test the creation of a Notification object. """
        self.assertIsInstance(self.notification, Notification)
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.question, self.question)
        self.assertEqual(self.notification.answer, self.answer)
        self.assertTrue(hasattr(self.notification, 'created_at'))

    def test_notification_str_method(self):
        """ Test the __str__ method of the Notification model. """
        expected_str = f'Notification for {self.user.username} about question {self.question.title}'
        self.assertEqual(str(self.notification), expected_str)


class ReportModelTest(TestCase):
    """ Test suite for the Report model. """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@aluno.unb.br', password='senha1010')
        cls.forum = Forum.objects.create( # pylint: disable=E1101
            title='Test Forum', description='Test Description')
        cls.question = Question.objects.create( # pylint: disable=E1101
            title='Test Question',
            description='Test Description',
            author=cls.user,
            forum=cls.forum
        )
        cls.answer = Answer.objects.create( # pylint: disable=E1101
            text='Test Answer',
            author=cls.user,
            question=cls.question
        )
        cls.report = Report.objects.create( # pylint: disable=E1101
            question=cls.question,
            user=cls.user,
            reason='ofensivo',
            details='Inappropriate content'
        )

    def test_report_creation(self):
        """ Test the creation of a Report object. """
        self.assertIsInstance(self.report, Report)
        self.assertEqual(self.report.question, self.question)
        self.assertEqual(self.report.user, self.user)
        self.assertEqual(self.report.reason, 'ofensivo')
        self.assertEqual(self.report.details, 'Inappropriate content')
        self.assertTrue(hasattr(self.report, 'created_at'))

    def test_report_str_method(self):
        """ Test the __str__ method of the Report model. """
        expected_str = f'Conteúdo ofensivo - {self.user.username} - Question'
        self.assertEqual(str(self.report), expected_str)
