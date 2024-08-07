# Generated by Django 4.2.3 on 2024-07-19 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='forum',
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='answer',
            name='description',
            field=models.TextField(default='Default description', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='answer',
            name='upvotes',
            field=models.IntegerField(default=0, verbose_name='Upvotes'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(verbose_name='Answer Text'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='Default description', verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('title', models.CharField(default='Default Title', max_length=100, verbose_name='Title')),
                ('favoritados', models.IntegerField(default=0, verbose_name='Favorited Count')),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('forum', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='main.forum', verbose_name='Forum')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='main.question', verbose_name='Question'),
        ),
    ]
