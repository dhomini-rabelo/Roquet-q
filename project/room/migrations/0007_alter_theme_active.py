# Generated by Django 3.2.7 on 2021-10-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0006_auto_20211013_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]