# Generated by Django 3.2.7 on 2021-11-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0011_alter_room_password_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='password_admin',
            field=models.CharField(default='admin', max_length=128, verbose_name='Senha (hash)'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
    ]