from django.shortcuts import render, get_object_or_404
from Support.code.apps._asks.ask import register_question, validate_question, verify_process__ask, delete_question, get_none_themes
from .support import get_questions_by_room_code
from rest_framework.decorators import api_view
from rest_framework.response import  Response
from rest_framework import  status, generics
from rest_framework.views import APIView
from .serializers import QuestionSerializer, VoteSerializer
from asks.models import Question
from room.models import Room
from django.db.models import Q, F
import json


test_header = {'token': 'adasdassd45a541da5d1sa51sa5ds1sda5', "Access-Control-Allow-Origin": "*"}




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
            response = dict(serializer.data) | {'status': 'valid'}
            return Response(response, status=status.HTTP_201_CREATED, headers = test_header)
        return Response(validation, status=status.HTTP_400_BAD_REQUEST,  headers = test_header)
    



class ListBestQuestionsView(APIView):

    def get(self, request, code):
        questions = get_questions_by_room_code(code, active=True)
        queryset = questions.filter(answered=False).annotate(score=F('up_votes')-F('down_votes')).order_by('-score')
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    
class ListFinalizedQuestions(APIView):
    def get(self, request, code):
        questions = get_questions_by_room_code(code, active=False)
        queryset = questions.annotate(score=F('up_votes')-F('down_votes')).order_by('-score')
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data)


class ListFinalizedAnsweredQuestions(APIView):
    def get(self, request, code):
        questions = get_questions_by_room_code(code, active=False)
        queryset = questions.filter(answered=True).annotate(score=F('up_votes')-F('down_votes')).order_by('-score')
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class QuestionDetailView(APIView):
    
    def get(self, request, code, id):
        question = get_object_or_404(get_questions_by_room_code(code, active=True), id=id)
        serializer = VoteSerializer(question)
        return Response(serializer.data)
    
    def put(self, request, code, id):
        question = get_object_or_404(get_questions_by_room_code(code, active=True), id=id)
        data = request.data 
        process = data.get('process')
        if isinstance(process, str):
            if process == 'up':
                question.up_votes += 1
            elif process == 'down':
                question.down_votes += 1
            elif process == 'mark':
                question.answered = True
            question.save()
            serializer = VoteSerializer(question)
            response = dict(serializer.data) | {'status': 'valid'}
            return Response(response, headers = test_header)
            
        return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
