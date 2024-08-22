# Generated by Django 4.2.14 on 2024-08-07 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_answer_image_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/answer_images/'),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/question_images/'),
        ),
    ]