from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, ManyToManyField, IntegerField, CASCADE, OneToOneField)
from django.db.models.signals import post_save
from room.models import Theme, Room


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
        
    
        
class UserKey(Model):
    key = CharField(max_length=550, verbose_name='Chave de usuário')
    room = ForeignKey(Room, on_delete=CASCADE, related_name='user_keys', verbose_name='Sala')

    class Meta:
        verbose_name = 'Chave de usuário'
        verbose_name_plural = 'Chave de usuários'
    
        
class AdminKey(Model):
    key = CharField(max_length=550, verbose_name='Chave de admin')
    room = ForeignKey(Room, on_delete=CASCADE, related_name='admin_keys', verbose_name='Sala')

    class Meta:
        verbose_name = 'Chave de administrador'
        verbose_name_plural = 'Chave de administradores'
    
    
class UsedKeys(Model):
    question = OneToOneField(Question, on_delete=CASCADE, related_name='used_keys', verbose_name='Pergunta')
    keys = ManyToManyField(UserKey, verbose_name='Chaves usadas por usuários para manipular contagem de votos')

    class Meta:
        verbose_name = 'Chaves usadas'
        verbose_name_plural = 'Chaves usadas'
       
       
def create_UsedKeys(sender, instance, created, **kwargs):
    if created == True:
        new_storage = UsedKeys.objects.create(question=instance)
        new_storage.save()
        


post_save.connect(create_UsedKeys, sender=Question)