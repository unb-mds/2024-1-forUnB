from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.questions.all()  # Retorna todas as perguntas associadas a este fórum


class Post(models.Model):
    description = models.TextField(verbose_name='Description', default='Default description')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Author', default=1)  # Substitua '1' pelo ID do usuário padrão
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')

    class Meta:
        abstract = True

    def __str__(self):
        return self.description[:50] + '...'
    
class Question(Post):
    title = models.CharField(max_length=100, verbose_name='Title', default='Default Title')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='questions', verbose_name='Forum', default=3)  # Substitua '3' pelo ID do fórum padrão, se aplicável
    favoritados = models.IntegerField(default=0, verbose_name='Favorited Count')

    def __str__(self):
        return self.title

class Answer(Post):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Question', default=1)  # Substitua '1' pelo ID da questão padrão, se aplicável
    upvotes = models.IntegerField(default=0, verbose_name='Upvotes')
    text = models.TextField(verbose_name='Answer Text')  # Incluindo o campo text explicitamente

    class Meta:
        """Classe pode ser usada no plural."""
        verbose_name_plural = 'answers'

    def __str__(self):
        """Visualização do text pelo banco de dados."""
        return self.text[:50] + '...'
