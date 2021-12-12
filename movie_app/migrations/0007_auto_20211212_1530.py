# Generated by Django 3.2.8 on 2021-12-12 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie_app', '0006_auto_20211212_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='unlikes',
            field=models.ManyToManyField(blank=True, related_name='comment_unlikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_app.comment')),
                ('likes', models.ManyToManyField(blank=True, related_name='reply_likes', to=settings.AUTH_USER_MODEL)),
                ('unlikes', models.ManyToManyField(blank=True, related_name='reply_unlikes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
