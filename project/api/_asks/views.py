from django.shortcuts import render, get_object_or_404
from Support.code.apps._asks.ask import register_question, validate_question, verify_process__ask, delete_question, get_none_themes
from .support import get_questions_by_room_code
from rest_framework.decorators import api_view
from rest_framework.response import  Response
from rest_framework import  status, generics
from rest_framework.views import APIView
from .serializers import QuestionSerializer, VoteSerializer
from asks.models import UsedKeys, UserKey, AdminKey, Question
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
        queryset = questions.annotate(score=F('up_votes')-F('down_votes')).order_by('-score', '-up_votes')
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data)


class ListFinalizedAnsweredQuestions(APIView):
    def get(self, request, code):
        questions = get_questions_by_room_code(code, active=False)
        queryset = questions.filter(answered=True).order_by('creation')
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class QuestionDetailView(APIView):
    
    def get(self, request, code, id):
        question = get_object_or_404(get_questions_by_room_code(code, active=True), id=id)
        serializer = VoteSerializer(question)
        return Response(serializer.data)
    
    def put(self, request, code, id):
        # counter hacks
        room = get_object_or_404(Room, code=code)
        question = get_object_or_404(Question, id=id)
        user_keys = UserKey.objects.filter(room=room).values_list('key', flat=True)
        admin_keys = AdminKey.objects.filter(room=room).values_list('key', flat=True)
        storage = UsedKeys.objects.get(question=question)
        used_keys = storage.keys.values_list('key', flat=True)
        
        data = request.data 
        process = data.get('process')
        key = data.get('key')
        
        if (isinstance(process, str) and isinstance(process, str)):
            if (process == 'up' and key in user_keys) and (key not in used_keys):
                question.up_votes += 1
                storage.keys.add(UserKey.objects.get(key=key))
            elif (process == 'down' and key in user_keys) and (key not in used_keys):
                question.down_votes += 1
                storage.keys.add(UserKey.objects.get(key=key))
            elif (process == 'pass' and key in user_keys) and (key not in used_keys):
                storage.keys.add(UserKey.objects.get(key=key))
            elif process == 'mark' and key in admin_keys:
                question.answered = True
            question.save()
            return Response({'status': 'success'}, headers = test_header)
            
        return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
