from Support.code.apps._room.create_room import get_room_code, create_an_room, create_admin_key
from Support.code.apps._room.enter_room import create_main_session, validate_room_entry
from Support.code.apps._room import send_errors_of_room, get_username_for_url
from Support.code.utils import field_exists
from django.shortcuts import redirect, render
from django.http import Http404
from .models import Room, Theme
from asks.models import Question
from time import sleep

BP = 'apps/room' # base path



def home(request):
    return render(request,f'{BP}/home.html')



def create_room(request):
    # initial flow
    context = dict()
    context['code'] = get_room_code()

    # main flow
    if request.method == 'GET':
        username = request.GET.get('username')
        context['username'] = username if username is not None else ''
    elif request.method == 'POST':
        operation = create_an_room(request)
        if operation['status'] == 'success':
            create_main_session(request, admin=True)
            create_admin_key(request, request.POST.get('code'))
            return redirect('settings', request.POST.get('code'))
        else:
            send_errors_of_room(request, operation['errors'])
            username = get_username_for_url(request)
            return redirect(f'/criar-sala{username}')
            
    return render(request, f'{BP}/create_room.html', context)



def enter_room(request):
    context = dict()
    if request.method == 'GET':
        username = request.GET.get('username')
        context['username'] = username if username is not None else ''
    
    elif request.method == 'POST':
        operation = validate_room_entry(request)
        if operation['status'] == 'success':
            create_main_session(request, admin=False)
            return redirect('ask', request.POST.get('code'))
        else:
            send_errors_of_room(request, operation['errors'])
            username = get_username_for_url(request)
            return redirect(f'/entrar-na-sala{username}')
        
    return render(request, f'{BP}/enter_room.html', context)



def code_room_shortcut(request, code):
    # initial flow
    if not field_exists(Room.objects, 'code', code):
        raise Http404
    
    context = dict()
    context['code'] = code
    
    
    # main flow    
    if request.method == 'POST':
        operation = validate_room_entry(request)
        if operation['status'] == 'success':
            create_main_session(request, admin=False)
            return redirect('ask', request.POST.get('code'))
        else:
            send_errors_of_room(request, operation['errors'])
            return redirect('code_room', code)
            
    return render(request, f'{BP}/code_room.html', context)



def logout(request):
    request.session.flush()
    return redirect('home')




# TESTS
TEST_CODE = 123456 # equal Support.tests.frontEnd.tests.QuestionCreationTest.code


def setUp_view(request): # works as a setUp for StaticLiveServerTestCase
    process = request.GET.get('process')
    if isinstance(process, str):
        if process == 'create_question':
            if TEST_CODE in Room.objects.values_list('code', flat=True):
                return render(request, 'blank.html')
            room = Room.objects.create(creator='admin_', code=TEST_CODE)
            theme = Theme.objects.create(creator='admin_', name='THEME_', room=room)
    return render(request, 'blank.html')
            
            
            
def test_result_view(request): # check test result
    process = request.GET.get('process')
    if isinstance(process, str):
        if process == 'create_question':
            sleep(15)
            room = Room.objects.filter(creator='admin_', code=TEST_CODE).first()
            assert room is not None
            themes_id = room.themes.values_list('id', flat=True)
            question_text = 'test_question' # equal  Support.tests.frontEnd.tests.QuestionCreationTest.send_question
            created_question = Question.objects.filter(text=question_text, theme__id__in=themes_id).first()
            assert created_question is not None 
    return render(request, 'blank.html')



def tearDown_view(request): # works as a tearDown for StaticLiveServerTestCase
    process = request.GET.get('process')
    if isinstance(process, str):
        if process == 'create_question':
            room = Room.objects.filter(creator='admin_', code=TEST_CODE).first()
            if room is not None:
                room.delete()
            
    return render(request, 'blank.html')
            
            
