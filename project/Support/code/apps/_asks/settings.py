from Support.code.apps._room.create_room import create_admin_key
from Support.code.utils import filters
from Support.code.checks import check_null
from Support.code.core import get_post_form_errors
from room.models import Theme, Room
from django.contrib import messages
from . import send_errors_of_asks
import hashlib


# SUPPORT FUNCTIONS


def exists_theme(request, theme_name: str):
    room = Room.objects.get(code=request.session['code'])
    theme = room.themes.filter(name=theme_name.upper()).first()
    
    if theme is not None:
        return True
    else:
        return False
   


def validate_theme_form(request):
    theme = filters(request.POST.get('theme'))
    
    fv = [
        [theme, 'str', 'theme', [('max_length', 128),]],
    ] 

    form_errors = get_post_form_errors(fv)

    if exists_theme(request, theme):
        return {'status': 'invalid', 'errors': 'Este tema já existe'}   
    elif form_errors is None:
        return {'status': 'valid'}
    else:
        return {'status': 'invalid', 'errors': form_errors}


# MAIN FUNCTIONS

def verify_process__settings(request):
    rp = request.POST
    action = filters(rp.get('action'))
    
    values = {'add': 'create theme', 'disable': 'disable theme', 'change': 'update for admin'}
    
    if not check_null(action):
        return {'action': values[action]}
    else: 
        return {'action': 'none'}
    


def create_theme(request, code):
    theme, user = filters(request.POST.get('theme')), request.session['main']['username']
    validation = validate_theme_form(request)

    if validation['status'] == 'valid': 
        current_room = Room.objects.get(code=code)
        new_theme = Theme.objects.create(name=theme.upper(), creator=user, active=True, room=current_room)
        new_theme.save()
    else:
        send_errors_of_asks(request, validation['errors'])



def disable_theme(request, code):
    theme_name = filters(request.POST.get('theme'))
    
    themes = Room.objects.get(code=code).themes.filter(active=True)
    theme = themes.get(name=theme_name)
    theme.active = False
    theme.save()
    
    
    
def try_update_for_admin(request, code):
    admin_password = Room.objects.get(code=code).password_admin
    password = filters(request.POST.get('password'))
    
    if isinstance(password, str) and admin_password == hashlib.md5(password.encode()).hexdigest():
        request.session['main']['admin'] = True
        create_admin_key(request, code)
        messages.success(request, 'Agora você é administrador')
    else:
        messages.error(request, 'Senha de administrador incorreta')
        
        
        
def get_total_of_questions(room):
    question_quantity = 0
    themes = room.themes.all()
    for theme in themes:
        question_quantity += theme.questions.count()
    return str(question_quantity)
    