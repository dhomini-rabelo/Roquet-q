from django.urls import path
from ._asks.views import CreateQuestionsView

urlpatterns = [
    path('criar-pergunta', CreateQuestionsView.as_view())
]