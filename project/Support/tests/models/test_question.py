from django.test import TestCase
from room.models import Theme, Room
from asks.models import Question
from unittest import expectedFailure
from datetime import datetime, timedelta



class QuestionTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(code=123456)
        self.theme = Theme.objects.create(name='test', room=self.room)
        self.question = Question.objects.create(creator='test', text='test', theme=self.theme) 
        self.question.save()
        
    def test_default_fields(self):
        self.assertEqual(self.question.answered, False)
        self.assertEqual(self.question.up_votes, 0)
        self.assertEqual(self.question.down_votes, 0)
        
    @expectedFailure
    def test_creator_size(self):
        # error because "max_length" was outdated
        self.question.creator = 'x' * 129
        self.question.save()

    def test_changes(self):
        self.assertEqual(self.question.creator, 'test')
        self.assertEqual(self.question.text, 'test')
        self.assertEqual(self.question.theme, self.theme)
        self.question.creator = 'new_creator'
        self.question.text = 'new_text'
        self.question.answered = True
        self.question.up_votes = 1
        self.question.down_votes = 2
        self.new_theme = Theme.objects.create(name='new_name', room=self.room)
        self.question.theme = self.new_theme
        self.question.save()
        self.assertEqual(self.question.creator, 'new_creator')
        self.assertEqual(self.question.text, 'new_text')
        self.assertEqual(self.question.answered, True)        
        self.assertEqual(self.question.up_votes, 1)
        self.assertEqual(self.question.down_votes, 2)               
        self.assertEqual(self.question.theme, self.new_theme)
        
    def test_verbose_name(self):
        model = self.question._meta
        self.assertEqual(model.get_field('creator').verbose_name, 'Criador')
        self.assertEqual(model.get_field('text').verbose_name, 'Texto')
        self.assertEqual(model.get_field('answered').verbose_name, 'Respondida')
        self.assertEqual(model.get_field('up_votes').verbose_name, 'Votos Positivos')
        self.assertEqual(model.get_field('down_votes').verbose_name, 'Votos Negativos')
        self.assertEqual(model.get_field('theme').verbose_name, 'Tema')

        
    def test_relationship__foreign_key(self):
        theme = Theme.objects.get(id=self.question.theme.id)
        self.assertIn(self.question, theme.questions.all())
        
    def tearDown(self):
        # type validation
        self.assertTrue(isinstance(self.question.creator, str))
        self.assertTrue(isinstance(self.question.text, str))
        self.assertTrue(isinstance(self.question.answered, bool))
        self.assertTrue(isinstance(self.question.creation, datetime))
        self.assertTrue(isinstance(self.question.up_votes, int))     
        self.assertTrue(isinstance(self.question.down_votes, int))     
  
        