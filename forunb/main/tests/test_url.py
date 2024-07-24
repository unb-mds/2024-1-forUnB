# tests/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import index, forum_detail, question_detail, questions, forum_list, new_question, new_answer
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_forum_detail_url_resolves(self):
        url = reverse('forum_detail', args=[1])
        self.assertEqual(resolve(url).func, forum_detail)

    def test_question_detail_url_resolves(self):
        url = reverse('question_detail', args=[1])
        self.assertEqual(resolve(url).func, question_detail)

    def test_questions_url_resolves(self):
        url = reverse('questions')
        self.assertEqual(resolve(url).func, questions)

    def test_forum_list_url_resolves(self):
        url = reverse('forum_list')
        self.assertEqual(resolve(url).func, forum_list)

    def test_new_question_url_resolves(self):
        url = reverse('new_question', args=[1])
        self.assertEqual(resolve(url).func, new_question)

    def test_new_answer_url_resolves(self):
        url = reverse('new_answer', args=[1])
        self.assertEqual(resolve(url).func, new_answer)

    # REVER COMO ESTÁ PARTE ESTÁ FUNCIONDO

    # def test_login_url_resolves(self):
    #     url = reverse('login')
    #     self.assertEqual(resolve(url).func.view_class, auth_views.LoginView.as_view())

    # def test_logout_url_resolves(self):
    #     url = reverse('logout')
    #     self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView.as_view())
