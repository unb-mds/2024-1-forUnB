""" This file contains the test class for checking URL resolution """
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import (
    index, forum_detail, question_detail, questions, forum_list, new_question,
    new_answer, user_posts, follow_forum, followed_forums, delete_question,
    delete_answer, notifications, toggle_upvote_question, toggle_upvote_answer, report
)

class TestUrls(SimpleTestCase):
    """ Test class for checking URL resolution """

    def test_index_url_resolves(self):
        """ Test if the 'index' URL correctly resolves to the 'index' view """
        url = reverse('main:index')
        self.assertEqual(resolve(url).func, index)

    def test_forum_detail_url_resolves(self):
        """ Test if the 'forum_detail' URL correctly resolves to the 'forum_detail' view """
        url = reverse('main:forum_detail', args=[1])
        self.assertEqual(resolve(url).func, forum_detail)

    def test_question_detail_url_resolves(self):
        """ Test if the 'question_detail' URL correctly resolves to the 'question_detail' view """
        url = reverse('main:question_detail', args=[1])
        self.assertEqual(resolve(url).func, question_detail)

    def test_questions_url_resolves(self):
        """ Test if the 'questions' URL correctly resolves to the 'questions' view """
        url = reverse('main:questions')
        self.assertEqual(resolve(url).func, questions)

    def test_forum_list_url_resolves(self):
        """ Test if the 'forum_list' URL correctly resolves to the 'forum_list' view """
        url = reverse('main:forum_list')
        self.assertEqual(resolve(url).func, forum_list)

    def test_new_question_url_resolves(self):
        """ Test if the 'new_question' URL correctly resolves to the 'new_question' view """
        url = reverse('main:new_question', args=[1])
        self.assertEqual(resolve(url).func, new_question)

    def test_new_answer_url_resolves(self):
        """ Test if the 'new_answer' URL correctly resolves to the 'new_answer' view """
        url = reverse('main:new_answer', args=[1])
        self.assertEqual(resolve(url).func, new_answer)

    def test_user_posts_url_resolves(self):
        """ Test if the 'user_posts' URL correctly resolves to the 'user_posts' view """
        url = reverse('main:user_posts')
        self.assertEqual(resolve(url).func, user_posts)

    def test_follow_forum_url_resolves(self):
        """ Test if the 'follow_forum' URL correctly resolves to the 'follow_forum' view """
        url = reverse('main:follow_forum', args=[1, 'follow'])
        self.assertEqual(resolve(url).func, follow_forum)

    def test_followed_forums_url_resolves(self):
        """ Test if the 'followed_forums' URL correctly resolves to the 'followed_forums' view """
        url = reverse('main:followed_forums')
        self.assertEqual(resolve(url).func, followed_forums)

    def test_delete_question_url_resolves(self):
        """ Test if the 'delete_question' URL correctly resolves to the 'delete_question' view """
        url = reverse('main:delete_question', args=[1])
        self.assertEqual(resolve(url).func, delete_question)

    def test_delete_answer_url_resolves(self):
        """ Test if the 'delete_answer' URL correctly resolves to the 'delete_answer' view """
        url = reverse('main:delete_answer', args=[1])
        self.assertEqual(resolve(url).func, delete_answer)

    def test_notifications_url_resolves(self):
        """ Test if the 'notifications' URL correctly resolves to the 'notifications' view """
        url = reverse('main:notifications')
        self.assertEqual(resolve(url).func, notifications)

    def test_toggle_upvote_question_url_resolves(self):
        """ 
        Test if the 'toggle_upvote_question' URL correctly resolves
        to the 'toggle_upvote_question' view
        """
        url = reverse('main:toggle_upvote_question', args=[1])
        self.assertEqual(resolve(url).func, toggle_upvote_question)

    def test_toggle_upvote_answer_url_resolves(self):
        """ 
        Test if the 'toggle_upvote_answer' URL correctly resolves 
        to the 'toggle_upvote_answer' view 
        """
        url = reverse('main:toggle_upvote_answer', args=[1])
        self.assertEqual(resolve(url).func, toggle_upvote_answer)

    def test_report_url_resolves(self):
        """ Test if the 'report' URL correctly resolves to the 'report' view """
        url = reverse('main:report', args=[1, 'question'])
        self.assertEqual(resolve(url).func, report)
