from django.urls import path
from ._asks.views import ListAndCreateQuestionsView, ListBestQuestionsView, QuestionDetailView, ListFinalizedQuestionsView, ListFinalizedAndAnsweredQuestionsView, DataRoomView

urlpatterns = [
    path('criar-perguntas', ListAndCreateQuestionsView.as_view()),
    path('dados-da-sala', DataRoomView.as_view()),
    path('lista-melhores-perguntas', ListBestQuestionsView.as_view()),
    path('lista-melhores-perguntas/<int:id>', QuestionDetailView.as_view()),
    path('lista-perguntas-finalizadas', ListFinalizedQuestionsView.as_view()),
    path('lista-perguntas-respondidas-finalizadas', ListFinalizedAndAnsweredQuestionsView.as_view()),
]