"""Models for the main app."""

from django.db import models
from django.conf import settings
from PIL import Image
from users.models import CustomUser
from cloudinary.models import CloudinaryField

if settings.DEBUG:
    ImageField = models.ImageField
else:
    from cloudinary.models import CloudinaryField
    ImageField = CloudinaryField

class Forum(models.Model):
    """Model for a forum."""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of a forum."""
        return str(self.title)

    def get_questions(self):
        """Returns all questions associated with this forum."""
        return self.questions.all()  # pylint: disable=E1101


class Post(models.Model):
    """Abstract model for a post."""
    description = models.TextField(verbose_name='')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='Author', default=1  # Substitua '1' pelo usuário padrão
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creation Date and Time'
    )

    class Meta: # pylint: disable=R0903
        """Meta class for Post."""
        abstract = True

    def __str__(self):
        """String representation of a post."""
        return str(self.description)[:50] + '...'


class Question(Post):
    """Model for a question."""
    title = models.CharField(max_length=100, verbose_name='')
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE,
        related_name='questions', verbose_name='Forum', default=3
    )
    favoritados = models.IntegerField(
        default=0, verbose_name='Favorited Count'
    )
    is_anonymous = models.BooleanField(default=False, verbose_name='')
    image = ImageField('image', blank=True, null=True)
    upvoters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='upvoted_questions', blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions'
    )

    def __str__(self):
        """String representation of a question."""
        return str(self.title)

    def save(self, *args, **kwargs):
        """Save method for a question."""
        super().save(*args, **kwargs)

        """if self.image:
            img = Image.open(self.image.path)  # pylint: disable=E1101
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)  # pylint: disable=E1101"""

    def toggle_upvote(self, user):
        """Toggles the upvote of a question for a user."""
        if user in self.upvoters.all():  # pylint: disable=E1101
            self.upvoters.remove(user)  # pylint: disable=E1101
        else:
            self.upvoters.add(user)  # pylint: disable=E1101
        self.save()

    @property
    def upvote_count(self):
        """Returns the number of upvotes for a question."""
        return self.upvoters.count()  # pylint: disable=E1101


class Answer(Post):
    """Model for an answer."""
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        related_name='answers', verbose_name='Question', default=1
    )
    text = models.TextField(verbose_name='Answer Text')
    is_anonymous = models.BooleanField(
        default=False, verbose_name='Modo anônimo'
    )
    image = ImageField('image', blank=True, null=True)
    upvoters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='upvoted_answers', blank=True
    )

    class Meta: # pylint: disable=R0903
        """Meta class for Answer."""
        verbose_name_plural = 'answers'

    def __str__(self):
        """String representation of an answer."""
        return str(self.text)[:50] + '...'

    def save(self, *args, **kwargs):
        """Save method for an answer."""
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)  # pylint: disable=E1101
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)  # pylint: disable=E1101

    def toggle_upvote(self, user):
        """Toggles the upvote of an answer for a user."""
        if user in self.upvoters.all():  # pylint: disable=E1101
            self.upvoters.remove(user)  # pylint: disable=E1101
        else:
            self.upvoters.add(user)  # pylint: disable=E1101
        self.save()

    @property
    def upvote_count(self):
        """Returns the number of upvotes for an answer."""
        return self.upvoters.count()  # pylint: disable=E1101


class Notification(models.Model):
    """Model for a notification."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of a notification."""
        return (
            f'Notification for {self.user.username} ' # pylint: disable=E1101
            f'about question {self.question.title}' # pylint: disable=E1101
        )


class Report(models.Model):
    """Model for a report."""
    REASON_CHOICES = [
        ('ofensivo', 'Conteúdo ofensivo'),
        ('irrelevante', 'Irrelevante para o fórum'),
        ('outros', 'Outros'),
    ]

    question = models.ForeignKey(
        'main.Question', on_delete=models.CASCADE, related_name='reports',
        null=True, blank=True
    )
    answer = models.ForeignKey(
        'main.Answer', on_delete=models.CASCADE, related_name='reports',
        null=True, blank=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of a report."""
        return (
            f"{self.get_reason_display()} - {self.user.username} - " # pylint: disable=E1101
            f"{'Question' if self.question else 'Answer'}" # pylint: disable=E1101
        )
