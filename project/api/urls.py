from django.urls import path
from ._asks.views import create_questions

urlpatterns = [
    path('criar-pergunta', create_questions)
]