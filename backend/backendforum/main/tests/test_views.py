from django.test import TestCase, Client
from django.urls import reverse

class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    # testa se a view index retorna um código de status HTTP 200, indicando que a página foi carregada com sucesso.
    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    
    # testa se a view index usa o template correto, 'main/index.html'.
    def test_index_view_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'main/index.html')