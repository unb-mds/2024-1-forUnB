from django.db import models

# Create your models here.


class Forum(models.Model):
    """Criação do modelo de Fórum."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Visualização do title pelo banco de dados."""
        return self.title


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
