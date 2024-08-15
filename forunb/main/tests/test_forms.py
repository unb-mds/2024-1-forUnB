""" Tests for the forms in the main app. """
from users.models import CustomUser
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from django.test import TestCase
from main.forms import *
from users.forms import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ForumFormTest(TestCase):
    """Tests for the forum creation form."""

    def test_forum_form_valid_data(self):
        """Tests if the form is valid with correct data."""
        form = ForumForm(data={'title': 'Test Forum',
                         'description': 'This is a test forum.'})
        self.assertTrue(form.is_valid())

    def test_forum_form_no_data(self):
        """Tests if the form is invalid without data."""
        form = ForumForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class QuestionFormTest(TestCase):
    """Tests for the question creation form."""

    def test_question_form_valid_data(self):
        """Tests if the form is valid with correct data."""
        form = QuestionForm(
            data={'title': 'Test Question', 'description': 'This is a test question.'})
        self.assertTrue(form.is_valid())

    def test_question_form_missing_title(self):
        """Tests if the form is invalid without a title."""
        form = QuestionForm(
            data={'description': 'This is a test question without a title.'})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class AnswerFormTest(TestCase):
    """Tests for the answer creation form."""

    def test_answer_form_valid_data(self):
        """Tests if the form is valid with correct data."""
        form = AnswerForm(data={'text': 'This is a test answer.'})
        self.assertTrue(form.is_valid())

    def test_answer_form_missing_text(self):
        """Tests if the form is invalid without text."""
        form = AnswerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)


class CustomUserFormTests(TestCase):
    """Tests for custom user forms."""

    def test_invalid_unb_email(self):
        """Tests if the form rejects an email that is not from UNB."""
        form_data = {'email': 'invalid@example.com',
                     'password1': 'password', 'password2': 'password'}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_valid_unb_email(self):
        """Tests if the form accepts a valid UNB email."""
        form_data = {'email': 'valid@aluno.unb.br',
                     'password1': 'password1010', 'password2': 'password1010'}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_user(self):
        """Tests if the form successfully creates a user."""
        form_data = {'email': 'valid@aluno.unb.br',
                     'password1': 'password1010', 'password2': 'password1010'}
        form = CustomUserCreationForm(data=form_data)
        if form.is_valid():
            user = form.save(commit=False)
            self.assertEqual(user.email, 'valid@aluno.unb.br')
            user.save()
            self.assertEqual(CustomUser.objects.count(), 1)
        else:
            self.fail(form.errors)

    def test_change_user(self):
        """Tests if the user change form allows updates."""
        user = CustomUser.objects.create_user(
            email='valid@aluno.unb.br', password='password')

        form_data = {
            'email': 'valid@aluno.unb.br',
            'username': 'newusername',
            'is_active': True,
            'is_staff': False
        }

        form = CustomUserChangeForm(data=form_data, instance=user)

        self.assertTrue(form.is_valid(), form.errors)
        updated_user = form.save(commit=False)
        self.assertEqual(updated_user.username, 'newusername')
        updated_user.save()

        user.refresh_from_db()
        self.assertEqual(user.username, 'newusername')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)


class ReportFormTest(TestCase):
    """Tests for the report form."""

    def test_report_form_valid_data(self):
        form = ReportForm(data={
            'reason': 'ofensivo',
            'details': 'This content is offensive.'
        })
        self.assertTrue(form.is_valid())

    def test_report_form_missing_reason(self):
        """Tests if the form is invalid without a reason."""
        form = ReportForm(data={
            'details': 'This content is offensive.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('reason', form.errors)

    def test_report_form_missing_details(self):
        """Tests if the form is valid even without details."""
        form = ReportForm(data={
            'reason': 'ofensivo',
        })
        self.assertTrue(form.is_valid())
