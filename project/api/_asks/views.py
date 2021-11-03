from django.shortcuts import render, get_object_or_404
from Support.code.apps._asks.ask import register_question, validate_question, verify_process__ask, delete_question, get_none_themes
from .support import get_questions_by_room_code
from rest_framework.decorators import api_view
from rest_framework.response import  Response
from .serializers import QuestionSerializer
from asks.models import Question
from room.models import Room


@api_view(['GET', 'POST'])
def create_questions(request, code):
    if request.method == 'GET':
        questions = get_questions_by_room_code(code)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass



