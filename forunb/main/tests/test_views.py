from django.test import TestCase, Client
from django.urls import reverse
from main.models import Forum, Question, Answer
from main.forms import ForumForm
from django.contrib.auth.models import User

# Testando esse modelo de teste
class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'main/index.html')
