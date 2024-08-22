# Generated by Django 4.2.13 on 2024-08-02 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_forum_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_anonymous',
            field=models.BooleanField(default=False, verbose_name='Anonymous'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_anonymous',
            field=models.BooleanField(default=False, verbose_name='Anonymous'),
        ),
    ]