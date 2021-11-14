from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('criar-sala', create_room, name='create_room'),
    path('entrar-na-sala', enter_room, name='enter_room'),
    path('sair', logout, name='logout'),
    path('<int:code>', code_room_shortcut, name='code_room'),
    path('<int:code>/', include('asks.urls')),
    # path('test/setUp', setUp_view),
    # path('test/result', test_result_view),
    # path('test/tearDown', tearDown_view),    
]
