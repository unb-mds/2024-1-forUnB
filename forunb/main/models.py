from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from users.models import CustomUser
from PIL import Image


# Create your models here.


class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.questions.all()  # Retorna todas as perguntas associadas a este fórum


class Post(models.Model): #descricao perguntas
    description = models.TextField(verbose_name='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Author', default=1)  # Substitua '1' pelo ID do usuário padrão
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')

    class Meta:
        abstract = True

    def __str__(self):
        return self.description[:50] + '...'
    
class Question(Post):
    title = models.CharField(max_length=100, verbose_name='')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='questions', verbose_name='Forum', default=3)
    favoritados = models.IntegerField(default=0, verbose_name='Favorited Count')
    is_anonymous = models.BooleanField(default=False, verbose_name='')
    image = models.ImageField(upload_to='media/question_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Answer(Post):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Question', default=1)
    upvotes = models.IntegerField(default=0, verbose_name='Upvotes')
    text = models.TextField(verbose_name='Answer Text')
    is_anonymous = models.BooleanField(default=False, verbose_name='Modo anônimo')
    image = models.ImageField(upload_to='media/answer_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'answers'

    def __str__(self):
        return self.text[:50] + '...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} about question {self.question.title}'