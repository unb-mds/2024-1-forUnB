from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    #photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followed_forums = models.ManyToManyField('main.Forum', blank=True, related_name='followers')
    liked_questions = models.ManyToManyField('main.Question', blank=True, related_name='liked_by')
    liked_answers = models.ManyToManyField('main.Answer', blank=True, related_name='liked_by')
    created_questions = models.ManyToManyField('main.Question', related_name='created_by')
    created_answers = models.ManyToManyField('main.Answer', related_name='created_by')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

