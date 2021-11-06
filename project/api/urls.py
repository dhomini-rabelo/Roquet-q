from django.urls import path
from ._asks.views import CreateQuestionsView, ListBestQuestionsView, QuestionDetailView, ListFinalizedQuestions, ListFinalizedAnsweredQuestions

urlpatterns = [
    path('criar-perguntas', CreateQuestionsView.as_view()),
    path('lista-melhores-perguntas', ListBestQuestionsView.as_view()),
    path('lista-perguntas-finalizadas', ListFinalizedQuestions.as_view()),
    path('lista-perguntas-respondidas-finalizadas', ListFinalizedAnsweredQuestions.as_view()),
    path('lista-melhores-perguntas/<int:id>', QuestionDetailView.as_view()),
]