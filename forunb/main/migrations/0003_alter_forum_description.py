# Generated by Django 4.2.13 on 2024-07-29 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_answer_forum_answer_author_answer_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
