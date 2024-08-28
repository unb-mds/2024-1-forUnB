""" This module contains the test suite for the views in the main app. """
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Forum, Question, Answer, Notification
from main.views import clean_html

User = get_user_model()

class IndexViewTestCase(TestCase):
    """ Test suite for the index view. """
    def setUp(self):
        """
        Set up the test environment with a user, forums, and questions.
        """
        self.client = Client()
        self.user = User.objects.create_user( # pylint: disable=E1101
            email='test@aluno.unb.br', password='senha1010'
        )
        self.forum1 = Forum.objects.create( # pylint: disable=E1101
            title="Python Programming", description="Discuss all things Python."
        )
        self.forum2 = Forum.objects.create( # pylint: disable=E1101
            title="Django Tips", description="Tips and tricks for Django."
        )
        self.question1 = Question.objects.create( # pylint: disable=E1101
            title="Python Question 1",
            description="Description for Python Question 1",
            forum=self.forum1,
            author=self.user  # Associando o usuário como autor
        )
        self.question2 = Question.objects.create( # pylint: disable=E1101
            title="Django Question 1",
            description="Description for Django Question 1",
            forum=self.forum2,
            author=self.user  # Associando o usuário como autor
        )

    def test_index_view_latest_questions(self):
        """
        Test that the index view returns the correct latest questions.
        """
        response = self.client.get(reverse('main:index') + '?filter_by=latest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, self.question1.title)
        self.assertContains(response, self.question2.title)

    def test_index_view_followed_forums(self):
        """
        Test that authenticated users see questions from followed forums.
        """
        self.user.followed_forums.add(self.forum1)
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.get(reverse('main:index') + '?filter_by=followed')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, self.question1.title)
        self.assertNotContains(response, self.question2.title)

    def test_index_view_followed_forums_redirect(self):
        """
        Test that unauthenticated users are redirected when trying to access followed forums.
        """
        response = self.client.get(reverse('main:index') + '?filter_by=followed')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('main:index')}")

    def test_index_view_status_code(self):
        """
        Test that the index view returns a status code of 200 (OK).
        """
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        """
        Test that the index view uses the correct template (main/index.html).
        """
        response = self.client.get(reverse('main:index'))
        self.assertTemplateUsed(response, 'main/index.html')


class ViewsTestCase(TestCase):
    """
    Test suite for various views in the main app.
    """

    def setUp(self):
        """
        Set up the test environment with a user, forum, question, and answer.
        """
        self.user = User.objects.create_user(
            email='test@aluno.unb.br', password='senha1010')
        self.forum = Forum.objects.create( # pylint: disable=E1101
            title="Test Forum", description="Test Forum Description")
        self.question = Question.objects.create( # pylint: disable=E1101
            title="Test Question",
            description="Test Question Description",
            forum=self.forum,
            author=self.user)
        self.answer = Answer.objects.create( # pylint: disable=E1101
            text="Test Answer", question=self.question, author=self.user)

    def test_index_view(self):
        """
        Test that the index view returns the correct response, uses the correct template,
        and contains the expected question title.
        """
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, self.question.title)

    def test_forum_detail_view(self):
        """
        Test that the forum detail view returns the correct response, uses the correct template,
        and contains the expected forum title.
        """
        response = self.client.get(
            reverse('main:forum_detail', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forum_detail.html')
        self.assertContains(response, self.forum.title)

    def test_forum_detail_view_least_upvoted(self):
        """Test that the forum detail view correctly orders questions by least upvoted."""
        # Cria perguntas com diferentes contagens de upvotes
        question2 = Question.objects.create(
            title="Another Test Question",
            description="Another Description",
            forum=self.forum,
            author=self.user
        )
        self.question.upvoters.add(self.user)  # Adiciona upvote à primeira pergunta

        response = self.client.get(
            reverse('main:forum_detail', args=[self.forum.id]) + '?order_by=least_upvoted')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forum_detail.html')
        questions = response.context['questions']
        self.assertEqual(questions[0], question2)  # A segunda pergunta deve aparecer primeiro

    def test_forum_detail_view_most_upvoted(self):
        """Test that the forum detail view correctly orders questions by most upvoted."""
        # Cria perguntas com diferentes contagens de upvotes
        question2 = Question.objects.create(
            title="Another Test Question",
            description="Another Description",
            forum=self.forum,
            author=self.user
        )
        self.question.upvoters.add(self.user)  # Adiciona upvote à primeira pergunta

        response = self.client.get(
            reverse('main:forum_detail', args=[self.forum.id]) + '?order_by=most_upvoted')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forum_detail.html')
        questions = response.context['questions']
        self.assertEqual(questions[0], self.question)  # A primeira pergunta deve aparecer primeiro

    def test_forum_detail_view_oldest(self):
        """Test that the forum detail view correctly orders questions by oldest first."""
        question2 = Question.objects.create(
            title="Another Test Question",
            description="Another Description",
            forum=self.forum,
            author=self.user
        )

        response = self.client.get(
            reverse('main:forum_detail', args=[self.forum.id]) + '?order_by=oldest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forum_detail.html')
        questions = response.context['questions']
        self.assertEqual(questions[0], self.question)  # A primeira pergunta criada deve aparecer primeiro

    def test_followed_forums_view(self):
        """Test that the followed forums view returns the correct followed forums for the user."""
        self.client.login(email='test@aluno.unb.br', password='senha1010')
        
        # Cria um fórum adicional e faz o usuário seguir ambos
        another_forum = Forum.objects.create(
            title="Another Forum", description="Another Forum Description")
        self.user.followed_forums.add(self.forum, another_forum)

        response = self.client.get(reverse('main:followed_forums'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forums.html')
        
        # Verifica se ambos os fóruns seguidos estão na resposta
        forums = response.context['forums']
        self.assertIn(self.forum, forums)
        self.assertIn(another_forum, forums)
        self.assertEqual(len(forums), 2)  # Certifica-se de que são exatamente dois fóruns seguidos

    def test_forum_list_view(self):
        """
        Test that the forum list view returns the correct response, uses the correct template,
        and contains the expected forum title.
        """
        response = self.client.get(reverse('main:forum_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forums.html')
        self.assertContains(response, self.forum.title)

    def test_clean_html_with_br_and_p_tags(self):
        """Test that clean_html correctly replaces <br> tags and preserves <p> tag formatting."""
        # Texto de entrada com tags <br> e <p>
        html_input = "<p>This is a paragraph.</p><br>And this is after a break.<br><p>New paragraph.</p>"
        
        # Texto esperado após a limpeza
        expected_output = "\nThis is a paragraph.\n\nAnd this is after a break.\n\nNew paragraph.\n"
        
        # Chama a função clean_html
        cleaned_text = clean_html(html_input)
        
        # Verifica se o texto limpo corresponde ao esperado
        self.assertEqual(cleaned_text, expected_output)

    def test_questions_view(self):
        """
        Test that the questions view returns the correct response, uses the correct template,
        and contains the expected question title.
        """
        response = self.client.get(reverse('main:questions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/questions.html')
        self.assertContains(response, self.question.title)

    def test_question_detail_view(self):
        """
        Test that the question detail view returns the correct response, uses the correct template,
        and contains the expected question title.
        """
        response = self.client.get(
            reverse('main:question_detail', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/question_detail.html')
        self.assertContains(response, self.question.title)

    def test_new_question_view(self):
        """
        Test that the new question view is accessible to logged-in users and that
        a new question can be posted via an AJAX request.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')
        response = self.client.get(
            reverse('main:new_question', args=[self.forum.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/new_question.html')

        response = self.client.post(reverse('main:new_question', args=[self.forum.id]), {
            'title': 'Another Test Question',
            'description': 'Another Test Question Description',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])
        self.assertIn('question_id', response_json)

    def test_new_question_invalid_form(self):
        """
        Test that the new_question view returns an error response when the form is invalid.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        # Enviar um formulário POST inválido
        response = self.client.post(reverse('main:new_question', args=[self.forum.id]), {
            'title': '',  # Título vazio para invalidar o formulário
            'description': '',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica se o status é 200 e se a resposta é a esperada (sucesso = False)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertFalse(response_json['success'])
        self.assertIn('errors', response_json)

    def test_new_answer_view(self):
        """
        Test that the new answer view is accessible to logged-in users and that
        a new answer can be posted via an AJAX request.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.get(
            reverse('main:question_detail', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/question_detail.html')

        response = self.client.post(reverse('main:new_answer', args=[self.question.id]), {
            'text': 'Another Test Answer',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])

    def test_follow_forum_view(self):
        """
        Test that a user can follow and unfollow a forum.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.post(
            reverse('main:follow_forum', args=[self.forum.id, 'follow']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.followed_forums.filter(
            id=self.forum.id).exists())

        response = self.client.post(
            reverse('main:follow_forum', args=[self.forum.id, 'unfollow']))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.followed_forums.filter(
            id=self.forum.id).exists())
        
    def test_follow_forum_view_invalid_method(self):
        """
        Test that follow_forum returns a 400 response when the request method is not POST.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        # Enviar uma requisição GET ao invés de POST
        response = self.client.get(reverse('main:follow_forum', args=[self.forum.id, 'follow']))

        # Verifica se o status é 400 e se a resposta é a esperada
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False})

    def test_user_posts_view(self):
        """
        Test that the user posts view returns the correct response, uses the correct template,
        and contains the expected question and answer.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.get(reverse('main:user_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/questions.html')
        self.assertContains(response, self.question.title)
        self.assertContains(response, self.answer.text)

    def test_delete_question_view(self):
        """
        Test that a user can delete their question, resulting in a redirect and
        the question being removed from the database.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.post(
            reverse('main:delete_question', args=[self.question.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Question.objects.filter(id=self.question.id).exists()) # pylint: disable=E1101

    def test_delete_answer_view(self):
        """
        Test that a user can delete their answer, resulting in a redirect and
        the answer being removed from the database.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.post(
            reverse('main:delete_answer', args=[self.answer.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Answer.objects.filter(id=self.answer.id).exists()) # pylint: disable=E1101

    def test_notifications_view(self):
        """
        Test that the notifications view returns the correct response, uses the correct template,
        and contains the expected notification content.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        Notification.objects.create( # pylint: disable=E1101
            user=self.user, question=self.question, answer=self.answer)

        response = self.client.get(reverse('main:notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/notifications.html')
        self.assertContains(response, self.question.title)

    def test_toggle_upvote_question_view(self):
        """
        Test that a user can toggle upvote on a question,
        increasing and decreasing the upvote count.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.post(
            reverse('main:toggle_upvote_question', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['upvotes'], 1)

        response = self.client.post(
            reverse('main:toggle_upvote_question', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['upvotes'], 0)

    def test_toggle_upvote_answer_view(self):
        """
        Test that a user can toggle upvote on an answer, increasing and decreasing the upvote count.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.post(
            reverse('main:toggle_upvote_answer', args=[self.answer.id]))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['upvotes'], 1)

        response = self.client.post(
            reverse('main:toggle_upvote_answer', args=[self.answer.id]))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['upvotes'], 0)

    def test_report_question_view(self):
        """
        Test that a user can report a question, resulting in a JSON response indicating success.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.post(reverse('main:report', args=[self.question.id, 'question']), {
            'reason': 'ofensivo',
            'details': 'Conteúdo inadequado',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])

    def test_report_answer_view(self):
        """
        Test that a user can report an answer, resulting in a JSON response indicating success.
        """
        self.client.login(email='test@aluno.unb.br', password='senha1010')

        response = self.client.post(reverse('main:report', args=[self.answer.id, 'answer']), {
            'reason': 'ofensivo',
            'details': 'Conteúdo inadequado',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])


class SearchForumTestCase(TestCase):
    """
    Test suite for the forum search functionality.
    """

    def setUp(self):
        """
        Set up the test environment with multiple forum objects.
        """
        self.client = Client()
        self.forum1 = Forum.objects.create( # pylint: disable=E1101
            title="Python Programming", description="Discuss all things Python.")
        self.forum2 = Forum.objects.create( # pylint: disable=E1101
            title="Django Tips", description="Tips and tricks for Django.")
        self.forum3 = Forum.objects.create( # pylint: disable=E1101
            title="Web Development", description="General web development discussion.")

    def test_search_forum_with_query(self):
        """
        Test that searching for a forum with a query
        returns the correct forum and uses the correct template.
        """
        response = self.client.get(
            reverse('search:search_forum') + '?search=python')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forums.html')
        self.assertIn('forums', response.context)
        forums = response.context['forums']
        self.assertEqual(len(forums), 1)
        self.assertEqual(forums[0], self.forum1)
        self.assertEqual(response.context['query'], 'python')

    def test_search_forum_with_no_results(self):
        """
        Test that searching for a forum with a query
        that returns no results uses the correct template
        and returns an empty list of forums.
        """
        response = self.client.get(
            reverse('search:search_forum') + '?search=java')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forums.html')
        self.assertIn('forums', response.context)
        forums = response.context['forums']
        self.assertEqual(len(forums), 0)
        self.assertEqual(response.context['query'], 'java')
