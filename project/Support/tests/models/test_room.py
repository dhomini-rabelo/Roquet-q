from django.test import TestCase
from unittest import expectedFailure
from room.models import Room, Theme



class RoomTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(code=123456)
        self.room.save()
        
    def test_default_fields(self):
        self.assertEqual(self.room.creator, '')
        self.assertEqual(self.room.password_admin, 'admin')
        self.assertEqual(self.room.visits, 0)
        
    @expectedFailure
    def test_creator_size(self):
        # error because "max_length" was outdated
        self.room.creator = 'x' * 129
        self.room.save()

    @expectedFailure
    def test_password_admin_size(self):
        # error because "max_length" was outdated
        self.room.password_admin = 'x' * 129
        self.room.save()

    def test_changes(self):
        self.assertEqual(self.room.code, 123456)
        self.room.creator = 'new_creator'
        self.room.password_admin = 'new_admin'
        self.room.code = 654321
        self.room.visits = 1
        self.room.save()
        self.assertEqual(self.room.creator, 'new_creator')
        self.assertEqual(self.room.password_admin, 'new_admin')
        self.assertEqual(self.room.code, 654321)
        self.assertEqual(self.room.visits, 1)        
        
    def test_verbose_name(self):
        model = self.room._meta
        self.assertEqual(model.get_field('creator').verbose_name, 'Criador')
        self.assertEqual(model.get_field('code').verbose_name, 'Código')
        self.assertEqual(model.get_field('password_admin').verbose_name, 'Senha (hash)')
        self.assertEqual(model.get_field('visits').verbose_name, 'Visitas')
        
    @expectedFailure
    def test_unique(self):
        # error because the code already exists
        new_room = Room.objects.create(code=123456)
        
    def test_str_method(self):
        self.assertEqual(str(self.room), f'Sala {self.room.code}')
        
    def test_relationship_many_to_1(self):
        self.assertEqual(list(self.room.themes.all()), [])
        theme_01 = Theme.objects.create(name='teste 01', room=self.room)
        theme_02 = Theme.objects.create(name='teste 02', room=self.room)
        self.room.themes.add(theme_01, theme_02)
        self.assertEqual(list(self.room.themes.all()), [theme_01, theme_02])
        
        
