# Generated by Django 5.0.4 on 2024-08-08 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_answer_upvoters_question_upvoters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='upvotes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='upvotes',
        ),
    ]