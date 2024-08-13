# tests/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import index, forum_detail, question_detail, questions, forum_list, new_question, new_answer, user_posts, follow_forum, followed_forums, delete_question, delete_answer, notifications, toggle_upvote_question, toggle_upvote_answer, report
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('main:index')
        self.assertEqual(resolve(url).func, index)

    def test_forum_detail_url_resolves(self):
        url = reverse('main:forum_detail', args=[1])
        self.assertEqual(resolve(url).func, forum_detail)

    def test_question_detail_url_resolves(self):
        url = reverse('main:question_detail', args=[1])
        self.assertEqual(resolve(url).func, question_detail)

    def test_questions_url_resolves(self):
        url = reverse('main:questions')
        self.assertEqual(resolve(url).func, questions)

    def test_forum_list_url_resolves(self):
        url = reverse('main:forum_list')
        self.assertEqual(resolve(url).func, forum_list)

    def test_new_question_url_resolves(self):
        url = reverse('main:new_question', args=[1])
        self.assertEqual(resolve(url).func, new_question)

    def test_new_answer_url_resolves(self):
        url = reverse('main:new_answer', args=[1])
        self.assertEqual(resolve(url).func, new_answer)

    def test_user_posts_url_resolves(self):
        url = reverse('main:user_posts')
        self.assertEqual(resolve(url).func, user_posts)

    def test_follow_forum_url_resolves(self):
        url = reverse('main:follow_forum', args=[1, 'follow'])
        self.assertEqual(resolve(url).func, follow_forum)

    def test_followed_forums_url_resolves(self):
        url = reverse('main:followed_forums')
        self.assertEqual(resolve(url).func, followed_forums)

    def test_delete_question_url_resolves(self):
        url = reverse('main:delete_question', args=[1])
        self.assertEqual(resolve(url).func, delete_question)

    def test_delete_answer_url_resolves(self):
        url = reverse('main:delete_answer', args=[1])
        self.assertEqual(resolve(url).func, delete_answer)

    def test_notifications_url_resolves(self):
        url = reverse('main:notifications')
        self.assertEqual(resolve(url).func, notifications)

    def test_toggle_upvote_question_url_resolves(self):
        url = reverse('main:toggle_upvote_question', args=[1])
        self.assertEqual(resolve(url).func, toggle_upvote_question)

    def test_toggle_upvote_answer_url_resolves(self):
        url = reverse('main:toggle_upvote_answer', args=[1])
        self.assertEqual(resolve(url).func, toggle_upvote_answer)

    def test_report_url_resolves(self):
        url = reverse('main:report', args=[1, 'question'])
        self.assertEqual(resolve(url).func, report)
    
