""" This file is used to register the models in the admin panel. """
from django.contrib import admin
from .models import Forum, Answer, Question, Report

# Register your models here.

admin.site.register(Forum)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Report)
