from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, CASCADE)
from django.db.models.fields.related import ManyToManyField

    
    
    
class Room(Model):
    creator = CharField(max_length=128, default='', verbose_name='Criador')
    code = PositiveIntegerField('Código', unique=True)
    password_admin = CharField('Senha (hash)', max_length=128, default='admin')
    visits = PositiveIntegerField('Visitas', default=0)
    

    def __str__(self):
        return f'Sala {self.code}'
    
    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'


class Theme(Model):
    creator = CharField(max_length=128, default='', verbose_name='Criador')
    name = CharField(max_length=128, verbose_name='Nome')
    active = BooleanField('Ativo', default=True)
    room = ForeignKey(Room, on_delete=CASCADE, related_name='themes', null=True, verbose_name='Sala')
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
