from django.urls import path
from ._asks.views import CreateQuestionsView, ListBestQuestionsView

urlpatterns = [
    path('criar-perguntas', CreateQuestionsView.as_view()),
    path('lista-melhores-perguntas', ListBestQuestionsView.as_view()),
]