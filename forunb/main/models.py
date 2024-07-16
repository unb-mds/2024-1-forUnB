from django.db import models

# Create your models here.
class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Answer(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'answers'
    def __str__(self):
        return self.text[:50] + '...'
