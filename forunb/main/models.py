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


class Answer(models.Model):
    """Modelo de perguntas para o fórum."""
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Classe pode ser usada no plural."""
        verbose_name_plural = 'answers'

    def __str__(self):
        """Visualização do text pelo banco de dados."""
        return self.text[:50] + '...'
