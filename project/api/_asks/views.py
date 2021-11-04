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


test_header = {"Access-Control-Allow-Origin": "*",'token': '12ad3sasd4ads56daasdaasdgt.dsa.aaadd'}


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
            return Response(json.dumps(serializer.data, indent = 4), status=status.HTTP_201_CREATED, headers = test_header)
        response = validation['errors']
        return Response(json.dumps(response, indent = 4), status=status.HTTP_400_BAD_REQUEST,  headers = test_header)
    
# function asyncPost(url, body) {
#     return fetch(url,{
#         method: "POST",
#         headers: {
#             "Content-Type": "application/json",
#         },
#         body: JSON.stringify(body)
#     }).then((data)=>data.json()).catch(error => {
#         console.error(error)
#       })
# }

# async function create_questions() {
#     let url = 'http://localhost:8000/api/123465/criar-pergunta'
#     let body = {
#     'creator': 'teste-de-js',
#     'text': 'apenas um teste js - pt 5',
#     'theme': 2
#     }
#     let response = await asyncPost(url, body)
#     response = JSON.parse(response)
#     console.log(response)
#     console.log(typeof response)
# }