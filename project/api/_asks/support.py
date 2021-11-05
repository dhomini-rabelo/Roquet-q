from django.shortcuts import render, get_object_or_404
from asks.models import Question
from room.models import Room, Theme



def get_questions_by_room_code(code, active=None):
    room = get_object_or_404(Room, code=code)
    if active is True:
        themes_id = room.themes.filter(active=True).values_list('id', flat=True) 
    elif active is False: 
        themes_id = room.themes.filter(active=False).values_list('id', flat=True) 
    else:
        themes_id = room.themes.values_list('id', flat=True)
    questions = Question.objects.filter(theme__id__in=themes_id)
    return questions
    