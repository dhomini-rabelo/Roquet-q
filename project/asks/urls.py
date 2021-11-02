from django.urls import path
from .views import *

urlpatterns = [
    path('perguntar', ask, name='ask'),
    path('votacao', vote, name='vote'),
    path('registros', records_view, name='records'),
    path('configuracoes', settings_view, name='settings'),
]
