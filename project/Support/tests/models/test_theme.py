from django.test import TestCase
from unittest import expectedFailure
from room.models import Theme, Room
from asks.models import Question



class ThemeTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(code=123456)
        self.theme = Theme.objects.create(name='test', room=self.room)
        self.theme.save()
        
    def test_default_fields(self):
        self.assertEqual(self.theme.creator, '')
        self.assertEqual(self.theme.active, True)
        
    @expectedFailure
    def test_size(self):
        # error because "max_length" was outdated
        word_test = 'x' * 129
        self.theme.name = word_test
        self.theme.creator = word_test
        self.theme.save()

    def test_changes(self):
        self.assertEqual(self.theme.creator, '')
        self.assertEqual(self.theme.name, 'test')
        self.assertEqual(self.theme.active, True)
        self.assertEqual(self.theme.room, self.room)
        self.theme.creator = 'new_creator'
        self.theme.name = 'new_test'
        self.theme.active = False
        self.new_room = Room.objects.create(code=654321)
        self.theme.room = self.new_room
        self.theme.save()
        self.assertEqual(self.theme.creator, 'new_creator')
        self.assertEqual(self.theme.name, 'new_test')
        self.assertEqual(self.theme.active, False)        
        self.assertEqual(self.theme.room, self.new_room)
        
    def test_verbose_name(self):
        model = self.theme._meta
        self.assertEqual(model.get_field('creator').verbose_name, 'Criador')
        self.assertEqual(model.get_field('name').verbose_name, 'Nome')
        self.assertEqual(model.get_field('active').verbose_name, 'Ativo')
        self.assertEqual(model.get_field('room').verbose_name, 'Sala')

    def test_str_method(self):
        self.assertEqual(str(self.theme), self.theme.name)
        
    def test_relationship_many_to_1(self):
        room = Room.objects.get(code=self.theme.room.code)
        self.assertIn(self.theme, room.themes.all())
        
    def test_relationship_many_to_many(self):
        self.assertEqual(list(self.theme.questions.all()), [])
        question_01 = Question.objects.create(creator='teste 01', text='teste1', theme=self.theme)
        question_02 = Question.objects.create(creator='teste 02', text='teste2', theme=self.theme)
        self.theme.questions.add(question_01, question_02)
        self.assertEqual(list(self.theme.questions.all()), [question_01, question_02])
