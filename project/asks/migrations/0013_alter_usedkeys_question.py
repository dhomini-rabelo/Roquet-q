# Generated by Django 3.2.7 on 2021-11-08 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asks', '0012_alter_usedkeys_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedkeys',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_keys', to='asks.question', verbose_name='Pergunta'),
        ),
    ]
