# Generated by Django 3.2.7 on 2021-10-19 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0007_alter_theme_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='polls',
        ),
    ]