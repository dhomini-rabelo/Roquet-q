from django.test import TestCase, Client
from unittest import expectedFailure
from room.models import Theme, Room
from asks.models import Question, UserKey, AdminKey, UsedKeys
import requests




class ResutsTest(TestCase):
    
    def setUp(self):
        self.room = Room.objects.create(code=123456)
        self.theme_01 = Theme.objects.create(name='tema 01', room=self.room)
        self.theme_02 = Theme.objects.create(name='tema 02', room=self.room)
        self.theme_03 = Theme.objects.create(name='tema 03', room=self.room, active=False)
        
        self.client = Client()
        self.themes_id = self.room.themes.values_list('id', flat=True)
        
        questions_theme_01 = []
        questions_theme_02 = []
        questions_theme_03 = []
        
        for i in range(1, 11):
            new_question_theme_01 = Question(creator=f'pergunta {i}', text=f'texto {i}', theme=self.theme_01)
            questions_theme_01.append(new_question_theme_01)
            new_question_theme_02 = Question(creator=f'pergunta {i+10}', text=f'texto {i+10}', theme=self.theme_02)
            questions_theme_02.append(new_question_theme_02)
            new_question_theme_03 = Question(creator=f'pergunta {i+20}', text=f'texto {i+20}', theme=self.theme_03)
            questions_theme_03.append(new_question_theme_03)
            new_question_theme_03 = Question(creator=f'pergunta {i+30}', text=f'texto {i+30}', theme=self.theme_03, answered=True)
            questions_theme_03.append(new_question_theme_03)
        
        all_questions = questions_theme_01[:] + questions_theme_02[:] + questions_theme_03[:]
        for question in all_questions: # for django_signals to work instead of using bulk_create
            question.save()
            
    
    def test_get_ListAndCreateQuestionsView(self):
        url = f'/api/{self.room.code}/criar-perguntas'
        request = self.client.get(url)
        response = request.json()
        # status test
        self.assertEqual(request.status_code, 200)
        # length test
        self.assertEqual(len(response), Question.objects.filter(theme__id__in=self.themes_id).count())
        # response structure test
        self.assertTrue(isinstance(response, list))
        self.assertTrue(isinstance(response[0], dict))
        self.assertEqual(list(response[0].keys()), ['creator', 'text', 'theme'])
        # type test
        self.assertTrue(isinstance(response[0]['creator'], str))
        self.assertTrue(isinstance(response[0]['text'], str))
        self.assertTrue(isinstance(response[0]['theme'], int))

