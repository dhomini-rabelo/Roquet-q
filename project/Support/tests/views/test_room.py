from Support.code.apps._room.create_room import get_room_code, create_an_room, create_admin_key
from Support.code.apps._room.enter_room import create_main_session, validate_room_entry
from Support.code.apps._room import send_errors_of_room, get_username_for_url
from Support.code.utils import field_exists
from django.shortcuts import redirect, render
from Support.code.validators import validate_unique
from Support.code.apps import generate_key
from django.http import Http404
from django.test import TestCase, Client
from unittest import expectedFailure
from room.models import Theme, Room
from asks.models import Question, UserKey, AdminKey



class RoomViewMethodsTest(TestCase):
    
    def setUp(self):     
        Room.objects.create(creator='admin_', code=654321)
        self.client = Client()
    
    def test_get_room_code(self):
        code = get_room_code()
        self.assertTrue(validate_unique(Room.objects, 'code', code))
        self.assertEqual(len(str(code)), 6)
        self.assertTrue(isinstance(code, int))
        
    def test_generate_key(self):
        key_test = generate_key()
        self.assertTrue(isinstance(key_test, str))
        self.assertTrue(len(key_test) in range(100, 500))
        user_keys = UserKey.objects.values_list('key', flat=True)
        admin_keys = AdminKey.objects.values_list('key', flat=True)
        used_keys = list(user_keys) + list(admin_keys)
        self.assertTrue(key_test not in used_keys)          
        
    def test_create_room_view(self):
        data = {
            'username': 'admin', 'password': 'password', 'code': '123456'
        }
        request = self.client.post('/criar-sala', data=data)
        # success test
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, '/123456/configuracoes')
        # db test
        room = Room.objects.get(code=123456)
        self.assertEqual(room.creator, 'admin')
        self.assertEqual(room.visits, 1)
  
    def test_enter_room_view(self):
        data = {
            'username': 'test', 'code': '654321'
        }
        request = self.client.post('/entrar-na-sala', data, follow=True)
        # success test
        self.assertEqual(request.status_code, 200)
        self.assertRedirects(request, '/654321/perguntar')

        
        
    def test_code_room_shortcut(self):
        data = {
            'username': 'test', 'code': '654321'
        }
        request = self.client.post('/654321', data=data, follow=True)
        # success test
        self.assertEqual(request.status_code, 200)
        self.assertRedirects(request, '/654321/perguntar')
    
    def test_logout(self):
        request = self.client.get('/sair')
        # success test
        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request, '/')

        