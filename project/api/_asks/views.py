from django.shortcuts import render, get_object_or_404
from Support.code.apps._asks.ask import register_question, validate_question, verify_process__ask, delete_question, get_none_themes
from .support import get_questions_by_room_code
from rest_framework.decorators import api_view
from rest_framework.response import  Response
from rest_framework import  status, generics
from rest_framework.views import APIView
from .serializers import QuestionSerializer
from asks.models import Question
from room.models import Room
import json


class CreateQuestionsView(APIView):

    def get(self, request, code):
        queryset = get_questions_by_room_code(code)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, code):
        validation = validate_question(request.data, code)
        serializer = QuestionSerializer(data=request.data)
        if validation['status'] == 'valid' and serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        response = validation['errors']
        return Response(response, status=status.HTTP_400_BAD_REQUEST)