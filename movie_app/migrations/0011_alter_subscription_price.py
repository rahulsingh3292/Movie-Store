# Generated by Django 3.2.8 on 2021-12-13 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0010_mysubscription_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.CharField(choices=[('199.99', '199.99'), ('399.99', '399.99'), ('999.99', '999.99')], max_length=50),
        ),
    ]
