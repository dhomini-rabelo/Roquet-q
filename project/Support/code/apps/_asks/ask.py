from Support.code.utils import filters
from Support.code.core import get_post_form_errors
from Support.code.validators import validate_unique
from . import send_errors_of_asks
from room.models import Theme, Room
from asks.models import Question
from django.contrib import messages
from datetime import datetime
from datetime import timedelta


# support functions

def exists_question(question, theme_id, code):
    room = Room.objects.get(code=code)
    theme_of_room = room.themes.get(id=theme_id)
    
    questions = list(item[0] for item in theme_of_room.questions.values_list('text'))
    
    if question in questions:
        return True
    return False


def verify_process__ask(request):
    allowed_process = ['delete_question', 'register_question']

    process = request.POST.get('process')
    
    if isinstance(process, str) and process in allowed_process:
        return {'action': process}                
    else:
        return {'action': 'none'}            


# main functions

def validate_question(rp, code):
    # rp -> request.POST
    room = Room.objects.get(code=code)
    creator, text = filters(rp.get('creator')), filters(rp.get('text'))
    theme = filters(rp.get('theme'))
    
    fv = [
        [creator, 'str', 'creator', [('max_length', 128)]],
        [text, 'str', 'text', [('max_length', 512)]],
        [theme, 'int', 'theme', [('exists', 'id')]],
    ]
    
    form_errors = get_post_form_errors(fv, room.themes.filter(active=True), api=True)
    
    if (form_errors is None) and (exists_question(text, theme, code)):
        return {'status': 'invalid', 'errors': {'text': 'Esta pergunta já foi cadastrada'}}
    elif form_errors is None:
        return {'status': 'valid', 'errors': {}}
    else:
        return {'status': 'invalid', 'errors': form_errors} 
    


def register_question(request, code):
    # main flow
    rp = request.POST
    username, question = filters(rp.get('username')), filters(rp.get('question'))
    theme = filters(rp.get('theme'))

    theme_of_question = Room.objects.get(code=code).themes.get(name=theme)
    new_question = Question.objects.create(creator=username, text=question, theme=theme_of_question)
    new_question.save()
    
    
    # end flow
    horary = new_question.creation - timedelta(hours=3)

    question = {
        'text': question, 'horary': horary.strftime('%H:%M'),
        'theme': theme, 'order': len(request.session['main']['my_questions'])
    }
    
    request.session['main']['my_questions'].insert(0, question)

        
        
        
def delete_question(request, code):
    rp = request.POST
    
    creator, text = filters(rp.get('creator')), filters(rp.get('text'))
    theme = filters(rp.get('theme'))
    
    theme = Room.objects.get(code=code).themes.get(name=theme)
    question = theme.questions.get(creator=creator, text=text)
    question.delete()
    messages.success(request, 'Pergunta excluída com sucesso')



def get_none_themes(request, themes):
    active_themes = [question['theme'] for question in request.session['main']['my_questions']]
    active_themes = list(set(active_themes))

    for theme in active_themes:
        themes.remove(theme)
    
    return themes