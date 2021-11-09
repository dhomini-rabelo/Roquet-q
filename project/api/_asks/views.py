from django.shortcuts import render, get_object_or_404
from Support.code.apps._asks.ask import register_question, validate_question, verify_process__ask, delete_question, get_none_themes
from Support.code.core import get_post_form_errors
from .support import get_questions_by_room_code
from rest_framework.response import  Response
from rest_framework import  status, generics
from rest_framework.views import APIView
from .serializers import QuestionForCreateSerializer, QuestionForVoteSerializer, DataRoomSerializer
from asks.models import UsedKeys, UserKey, AdminKey, Question
from room.models import Room
from django.db.models import Q, F
import json
from pprint import pprint





class ListAndCreateQuestionsView(APIView):

    def get(self, request, code):
        queryset = get_questions_by_room_code(code)
        serializer = QuestionForCreateSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, code):
        validation = validate_question(request.data, code)
        serializer = QuestionForCreateSerializer(data=request.data)
        if validation['status'] == 'valid' and serializer.is_valid():
            serializer.save()
            response = dict(serializer.data) | {'status': 'valid'}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(validation, status=status.HTTP_400_BAD_REQUEST)
    



class ListBestQuestionsView(APIView):

    def get(self, request, code):
        questions = get_questions_by_room_code(code, active=True)
        queryset = questions.filter(answered=False).annotate(score=F('up_votes')-F('down_votes')).order_by('-score')
        serializer = QuestionForVoteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    
class ListFinalizedQuestionsView(APIView):
    def get(self, request, code):
        questions = get_questions_by_room_code(code, active=False)
        queryset = questions.annotate(score=F('up_votes')-F('down_votes')).order_by('-score', '-up_votes')
        serializer = QuestionForVoteSerializer(queryset, many=True)
        return Response(serializer.data)


class ListFinalizedAndAnsweredQuestionsView(APIView):
    def get(self, request, code):
        questions = get_questions_by_room_code(code, active=False)
        queryset = questions.filter(answered=True).order_by('creation')
        serializer = QuestionForVoteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class QuestionDetailView(APIView):
    
    def get(self, request, code, id):
        question = get_object_or_404(get_questions_by_room_code(code, active=True), id=id)
        serializer = QuestionForVoteSerializer(question)
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
        
        fv = [
            [data, 'str', 'data', []],
            [key, 'str', 'data', []],
        ]
        
        errors = get_post_form_errors(fv, api=True)
        
        if (isinstance(process, str) and isinstance(process, str)):
            if process in ['up', 'down', 'pass']:
                if key not in user_keys:
                    return Response({'key': 'Chave não identificada'}, status=status.HTTP_400_BAD_REQUEST) 
                elif key not in used_keys:
                    return Response({'key': 'Chave já foi usada'}, status=status.HTTP_400_BAD_REQUEST) 
                
                if process == 'up':
                    question.up_votes += 1
                elif process == 'down':
                    question.down_votes += 1
                    
                storage.keys.add(UserKey.objects.get(key=key))
                    
                question.save()
                    
            elif process == 'mark':
                if key not in admin_keys:
                    return Response({'key': 'Você não tem permissão para fazer isso'}, status=status.HTTP_400_BAD_REQUEST) 
                question.answered = True
                question.save()
                
            return Response({'status': 'success'})
            
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)




class DataRoomView(APIView):
    
    def get(self, request, code):
        room = get_object_or_404(Room, code=code)
        serializer = DataRoomSerializer(room)
        response = dict(serializer.data)
        total_of_questions = 0
        
        for index, theme in enumerate(response['themes']):
            total_questions_of_theme = len(theme['questions'])
            response['themes'][index]['questions'] = total_questions_of_theme
            total_of_questions += total_questions_of_theme
            
        response['all_questions'] = total_of_questions
            
        return Response(response)