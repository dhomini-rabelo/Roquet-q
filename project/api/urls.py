from django.urls import path
from ._asks.views import CreateQuestionsView

urlpatterns = [
    path('criar-perguntas', CreateQuestionsView.as_view())
]