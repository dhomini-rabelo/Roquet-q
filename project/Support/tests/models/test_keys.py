from django.test import TestCase
from unittest import expectedFailure
from room.models import Theme, Room
from asks.models import Question, UserKey, AdminKey, UsedKeys



class UserKeyTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(code=123456)
        self.user_key = UserKey.objects.create(key='test', room=self.room)
        self.user_key.save()
        
    @expectedFailure
    def test_key_size(self):
        # error because "max_length" was outdated
        self.user_key.key = 'x' * 551
        self.user_key.save()

    def test_changes(self):
        self.assertEqual(self.user_key.key, 'test')
        self.assertEqual(self.user_key.room, self.room)
        self.user_key.key = 'new_key'
        self.new_room = Room.objects.create(code=654321)
        self.user_key.room = self.new_room
        self.user_key.save()
        self.assertEqual(self.user_key.key, 'new_key')       
        self.assertEqual(self.user_key.room, self.new_room)
        
    def test_verbose_name(self):
        model = self.user_key._meta
        self.assertEqual(model.get_field('key').verbose_name, 'Chave de usuário')
        self.assertEqual(model.get_field('room').verbose_name, 'Sala')
        
    def test_relationship_foreign_key(self):
        room = Room.objects.get(code=self.user_key.room.code)
        self.assertIn(self.user_key, room.user_keys.all())


class AdminKeyTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(code=123456)
        self.admin_key = AdminKey.objects.create(key='test', room=self.room)
        self.admin_key.save()
        
    @expectedFailure
    def test_key_size(self):
        # error because "max_length" was outdated
        self.admin_key.key = 'x' * 551
        self.admin_key.save()

    def test_changes(self):
        self.assertEqual(self.admin_key.key, 'test')
        self.assertEqual(self.admin_key.room, self.room)
        self.admin_key.key = 'new_key'
        self.new_room = Room.objects.create(code=654321)
        self.admin_key.room = self.new_room
        self.admin_key.save()
        self.assertEqual(self.admin_key.key, 'new_key')       
        self.assertEqual(self.admin_key.room, self.new_room)
        
    def test_verbose_name(self):
        model = self.admin_key._meta
        self.assertEqual(model.get_field('key').verbose_name, 'Chave de admin')
        self.assertEqual(model.get_field('room').verbose_name, 'Sala')
        
    def test_relationship_foreign_key(self):
        room = Room.objects.get(code=self.admin_key.room.code)
        self.assertIn(self.admin_key, room.admin_keys.all())


class UsedKeysTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(code=123456)
        self.theme = Theme.objects.create(name='test', room=self.room)
        self.question = Question.objects.create(creator='test', text='test', theme=self.theme)         
        self.used_keys = UsedKeys.objects.get(question=self.question)
        self.used_keys.save()
   
    def test_verbose_name(self):
        model = self.used_keys._meta
        self.assertEqual(model.get_field('question').verbose_name, 'Pergunta')
        self.assertEqual(model.get_field('keys').verbose_name, 'Chaves usadas')
        
    def test_relationship_one_to_one(self):
        question = Question.objects.get(id=self.used_keys.question.id)
        self.assertEqual(self.used_keys, question.used_keys)
        self.assertEqual(question, self.used_keys.question)
        
    def test_relationship_many_to_many(self):
        self.assertEqual(list(self.used_keys.keys.all()), [])
        self.question2 = Question.objects.create(creator='test2', text='test2', theme=self.theme)  
        user_key_01 = UserKey.objects.create(key='teste 01', room=self.room)
        user_key_02 = UserKey.objects.create(key='teste 02', room=self.room)
        self.used_keys.keys.add(user_key_01, user_key_02)
        self.question2.used_keys.keys.add(user_key_01, user_key_02)
        self.assertEqual(list(self.used_keys.keys.all()), [user_key_01, user_key_02])        
        self.assertEqual(list(self.question2.used_keys.keys.all()), [user_key_01, user_key_02])        
        
        