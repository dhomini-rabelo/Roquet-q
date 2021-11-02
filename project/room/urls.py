from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('criar-sala', create_room, name='create_room'),
    path('entrar-na-sala', enter_room, name='enter_room'),
    path('sair', logout, name='logout'),
    path('<int:code>', code_room_shortcut, name='code_room'),
    path('<int:code>/', include('asks.urls')),
]
