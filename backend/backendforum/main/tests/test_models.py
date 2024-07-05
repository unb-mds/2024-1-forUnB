from django.test import TestCase

from main.models import *

# Create your tests here.

class ForumModelTest (TestCase):

    def setUpTestData():
        Forum.objects.create(title='Cálculo 1', description='Isso é um teste', created_at='Data de Adição: Apr 27, 2024 22:06')

    
    def test_title_name_label(self):
        forum = Forum.objects.get(id=1)
        field_label = forum._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_name_max_lenght(self):
        forum = Forum.objects.get(id=1)
        max_length = forum._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_string_return(self):
        forum = Forum.objects.get(id=1)
        self.assertEquals(forum.__str__(), 'Cálculo 1')