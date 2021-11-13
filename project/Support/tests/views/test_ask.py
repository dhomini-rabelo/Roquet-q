from django.shortcuts import render, redirect
from Support.code.apps._asks.decorators import main_sessions_required
from Support.code.apps._asks.settings import verify_process__settings, create_theme, try_update_for_admin, disable_theme, get_total_of_questions
from Support.code.apps._asks.ask import delete_question
from Support.code.apps import generate_key
from django.http import Http404
from django.test import TestCase, Client, tag
from unittest import expectedFailure
from room.models import Theme, Room
from asks.models import Question, UserKey, AdminKey




class AskViewMethodsTest(TestCase):
    
    def setUp(self):     
        self.room = Room.objects.create(creator='admin_', code=654321)
        self.theme = Theme.objects.create(creator='admin_', name='theme_test', room=self.room)
        self.question = Question.objects.create(creator='admin_', text='text_test', theme=self.theme)
        self.client = Client()
        # login
        login_data = {
            'username': 'test', 'code': '654321'
        }
        request = self.client.post('/entrar-na-sala', data=login_data, follow=True)
        self.assertEqual(request.status_code, 200)
        self.assertRedirects(request, '/654321/perguntar')        
        

    def test_delete_question(self):
        question_for_delete_test = {
            'creator': 'admin_', 'text': 'text_test', 'theme': 'theme_test'
        }
        request = self.client.post('/654321/perguntar', data=question_for_delete_test, follow=True)
        self.assertEqual(request.status_code, 200)
        self.assertIsNone(Question.objects.filter(creator='admin_', text='text_test', theme=self.theme).first())
        
    def test_create_theme(self):
        new_theme = {
            'theme': 'theme_test_1', 'action': 'add'
        }
        request = self.client.post('/654321/configuracoes', data=new_theme, follow=True)
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(Theme.objects.filter(name='THEME_TEST_1', active=True).first())

    def test_disable_theme(self):
        theme = {
            'theme': 'theme_test', 'action': 'disable'
        }
        request = self.client.post('/654321/configuracoes', data=theme, follow=True)
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(Theme.objects.filter(name='theme_test', active=False).first())
        
