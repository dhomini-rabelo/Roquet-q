from Support.code.core import get_post_form_errors
from Support.code.utils import filters
from room.models import Room



def validate_room_entry(request):
    rp = request.POST
    
    username, code = filters(rp.get('username')),  rp.get('code') 

    fv = [
        [username, 'str', 'username', []],
        [code, 'int', 'code', [('equal_length', 6), ('exists', 'code')]],
    ]
    
    form_errors = get_post_form_errors(fv, Room.objects)
    
    if form_errors is None:
        return {'status': 'success'}
    else:
        return {'status': 'error', 'errors': form_errors}



def create_main_session(request, admin=False):
    username = request.POST.get('username')
    code = request.POST.get('code')
        
    request.session.flush()
    request.session['main'] = {
        'username': username, 'admin': admin,
        'my_questions': [], 'voted_questions': []
    }
    request.session['code'] = code
    room = Room.objects.get(code=code)
    room.visits += 1
    room.save()
    