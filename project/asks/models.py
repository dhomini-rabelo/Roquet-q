from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, ManyToManyField, IntegerField, CASCADE)
from room.models import Theme


class Question(Model):
    creator = CharField(max_length=128, verbose_name='Criador')
    text = TextField(max_length=512, verbose_name='Texto')
    answered = BooleanField('Respondida', default=False)
    creation = DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    up_votes = PositiveIntegerField('Votos Positivos', default=0)
    down_votes = PositiveIntegerField('Votos Negativos', default=0)
    theme = ForeignKey(Theme, on_delete=CASCADE, related_name='questions', null=True, verbose_name='Tema')
    
    class Meta:
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'
       
      