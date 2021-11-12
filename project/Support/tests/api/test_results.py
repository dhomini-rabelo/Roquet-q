from django.test import TestCase, Client
from django.db.models import F
from unittest import expectedFailure
from room.models import Theme, Room
from asks.models import Question, UserKey, AdminKey, UsedKeys
from datetime import datetime
import json




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

    def test_get_ListBestQuestionsView(self):
        url = f'/api/{self.room.code}/lista-melhores-perguntas'
        request = self.client.get(url)
        response = request.json()
        # status test
        self.assertEqual(request.status_code, 200)
        # length test
        queryset = Question.objects.filter(answered=False, theme__id__in=self.themes_id, theme__active=True)
        self.assertEqual(len(response), queryset.count())        
        # response structure test
        self.assertTrue(isinstance(response, list))
        self.assertTrue(isinstance(response[0], dict))
        self.assertEqual(list(response[0].keys()), ['id', 'creator', 'text', 'theme', 'up_votes', 'down_votes', 'creation', 'answered'])
        # type test
        self.assertTrue(isinstance(response[0]['id'], int))
        self.assertTrue(isinstance(response[0]['creator'], str))
        self.assertTrue(isinstance(response[0]['text'], str))
        self.assertTrue(isinstance(response[0]['theme'], int))
        self.assertTrue(isinstance(response[0]['up_votes'], int))
        self.assertTrue(isinstance(response[0]['down_votes'], int))
        self.assertTrue(isinstance(response[0]['answered'], bool))

    def test_get_ListFinalizedQuestionsView(self):
        url = f'/api/{self.room.code}/lista-perguntas-finalizadas'
        request = self.client.get(url)
        response = request.json()
        # status test
        self.assertEqual(request.status_code, 200)
        # length test
        queryset = Question.objects.filter(theme__id__in=self.themes_id, theme__active=False)
        self.assertEqual(len(response), queryset.count())        
        # response structure test
        self.assertTrue(isinstance(response, list))
        self.assertTrue(isinstance(response[0], dict))
        self.assertEqual(list(response[0].keys()), ['id', 'creator', 'text', 'theme', 'up_votes', 'down_votes', 'creation', 'answered'])
        # type test
        self.assertTrue(isinstance(response[0]['id'], int))
        self.assertTrue(isinstance(response[0]['creator'], str))
        self.assertTrue(isinstance(response[0]['text'], str))
        self.assertTrue(isinstance(response[0]['theme'], int))
        self.assertTrue(isinstance(response[0]['up_votes'], int))
        self.assertTrue(isinstance(response[0]['down_votes'], int))
        self.assertTrue(isinstance(response[0]['answered'], bool))
        
    def test_get_ListFinalizedAndAnsweredQuestionsView(self):
        url = f'/api/{self.room.code}/lista-perguntas-respondidas-finalizadas'
        request = self.client.get(url)
        response = request.json()
        # status test
        self.assertEqual(request.status_code, 200)
        # length test
        queryset = Question.objects.filter(theme__id__in=self.themes_id, answered=True, theme__active=False)
        self.assertEqual(len(response), queryset.count())        
        # response structure test
        self.assertTrue(isinstance(response, list))
        self.assertTrue(isinstance(response[0], dict))
        self.assertEqual(list(response[0].keys()), ['id', 'creator', 'text', 'theme', 'up_votes', 'down_votes', 'creation', 'answered'])
        # type test
        self.assertTrue(isinstance(response[0]['id'], int))
        self.assertTrue(isinstance(response[0]['creator'], str))
        self.assertTrue(isinstance(response[0]['text'], str))
        self.assertTrue(isinstance(response[0]['theme'], int))
        self.assertTrue(isinstance(response[0]['up_votes'], int))
        self.assertTrue(isinstance(response[0]['down_votes'], int))
        self.assertTrue(isinstance(response[0]['answered'], bool))

    def test_get_QuestionDetailView(self):
        question = Question.objects.get(creator='pergunta 1')
        url = f'/api/{self.room.code}/lista-melhores-perguntas/{question.id}'
        request = self.client.get(url)
        response = request.json()
        # status test
        self.assertEqual(request.status_code, 200)   
        # response structure test
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(list(response.keys()), ['id', 'creator', 'text', 'theme', 'up_votes', 'down_votes', 'creation', 'answered'])
        # type test
        self.assertTrue(isinstance(response['id'], int))
        self.assertTrue(isinstance(response['creator'], str))
        self.assertTrue(isinstance(response['text'], str))
        self.assertTrue(isinstance(response['theme'], int))
        self.assertTrue(isinstance(response['up_votes'], int))
        self.assertTrue(isinstance(response['down_votes'], int))
        self.assertTrue(isinstance(response['answered'], bool))
        # values test
        self.assertEqual(response['id'], question.id)
        self.assertEqual(response['creator'], question.creator)
        self.assertEqual(response['text'], question.text)        
        self.assertEqual(response['theme'], question.theme.id)
        self.assertEqual(response['up_votes'], question.up_votes)
        self.assertEqual(response['down_votes'], question.down_votes)
        self.assertEqual(response['answered'], question.answered)
        
    def test_get_DataRoomView(self):
        url = f'/api/{self.room.code}/dados-da-sala'
        request = self.client.get(url)
        response = request.json()
        questions = Question.objects.filter(theme__id__in=self.themes_id)
        # status test
        self.assertEqual(request.status_code, 200)   
        # response structure test
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(list(response.keys()), ['creator', 'visits', 'all_questions', 'themes'])
        # type test
        self.assertTrue(isinstance(response['creator'], str))
        self.assertTrue(isinstance(response['visits'], int))
        self.assertTrue(isinstance(response['all_questions'], int))
        self.assertTrue(isinstance(response['themes'], list))
        # values test
        self.assertEqual(response['creator'], self.room.creator)
        self.assertEqual(response['visits'], self.room.visits)        
        self.assertEqual(response['all_questions'], questions.count())
        # themes size test
        self.assertEqual(len(response['themes']), len(self.themes_id))
        # themes values test
        for index, theme_id in enumerate(list(self.themes_id)): # order -> id
            theme = Theme.objects.get(id=theme_id)
            self.assertEqual(response['themes'][index]['name'], theme.name)
            self.assertEqual(response['themes'][index]['creator'], theme.creator)
            self.assertEqual(response['themes'][index]['questions'], theme.questions.count())
            self.assertEqual(response['themes'][index]['active'], theme.active)
    