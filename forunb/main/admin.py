from django.contrib import admin
from .models import Forum, Answer, Question, Report

admin.site.register(Forum)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Report)

# Register your models here.

