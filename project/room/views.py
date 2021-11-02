from Support.code.apps._room.create_room import get_room_code, create_an_room
from Support.code.apps._room.enter_room import create_main_session, validate_room_entry
from Support.code.apps._room import send_errors_of_room
from Support.code.utils import field_exists
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from .models import Room


BP = 'apps/room' # base path



def home(request):
    print(request.__dir__())
    return render(request,f'{BP}/home.html')



def create_room(request):
    # initial flow
    context = dict()
    context['code'] = get_room_code()

    # main flow
    if request.method == 'POST':
        operation = create_an_room(request)
        if operation['status'] == 'success':
            create_main_session(request, admin=True)
            return redirect('settings', request.POST.get('code'))
        else:
            send_errors_of_room(request, operation['errors'])
            return redirect('create_room')
            
    return render(request, f'{BP}/create_room.html', context)



def enter_room(request):
    if request.method == 'POST':
        operation = validate_room_entry(request)
        if operation['status'] == 'success':
            create_main_session(request, admin=False)
            return redirect('ask', request.POST.get('code'))
        else:
            send_errors_of_room(request, operation['errors'])
            return redirect('enter_room')
        
    return render(request, f'{BP}/enter_room.html')



def code_room_shortcut(request, code):
    # initial flow
    if not field_exists(Room, 'code', code):
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