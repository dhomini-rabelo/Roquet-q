from django.shortcuts import render, get_object_or_404
from asks.models import Question
from room.models import Room, Theme



def get_questions_by_room_code(code):
    room = get_object_or_404(Room, code=code)
    themes_id = room.themes.values_list('id', flat=True)
    questions = Question.objects.filter(theme__id__in=themes_id)
    return questions
    