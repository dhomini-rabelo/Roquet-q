from django.shortcuts import render, redirect
from Support.code.apps._asks import user_permission
from Support.code.apps._asks.decorators import main_sessions_required
from Support.code.apps._asks.settings import verify_process__settings, create_theme, try_update_for_admin, disable_theme, get_total_of_questions
from Support.code.apps._asks.records import get_questions_answered, get_questions_for_end_rank
from Support.code.apps._asks.ask import register_question, validate_question, verify_process__ask, delete_question, get_none_themes
from Support.code.apps._asks import send_errors_of_asks
from Support.code.apps._asks.vote import select_questions, register_vote, get_best_questions, get_last_voted_theme
from room.models import Room
from django.contrib import messages


BP = 'apps/asks' # base path


@main_sessions_required
def ask(request, code):
    # initial flow
      
    if request.method == 'GET':
        context = dict()
        context['code'] = code
        context['username'] = request.session['main']['username']
        context['themes'] = Room.objects.get(code=code).themes.filter(active=True)
        context['my_questions'] = request.session['main']['my_questions']
        context['none_themes'] = get_none_themes(request, list(context['themes'].values_list('name', flat=True)))


    # main flow
    elif request.method == 'POST':
        process = verify_process__ask(request)
        
        if process['action'] == 'register_question':
            operation = validate_question(request.POST, code)
            if operation['response'] == 'valid':
                register_question(request, code)
                messages.success(request, 'Pergunta registrada com sucesso')
            elif operation['response'] == 'invalid':        
                send_errors_of_asks(request, operation['errors'])
                
                
        elif process['action'] == 'delete_question':
            delete_question(request)
            
        return redirect('ask', code)
    
    # end flow 
    context['selected'] = context['my_questions'][0]['theme'] if len(context['my_questions']) else 'none'
    
    return render(request, f'{BP}/ask.html', context)



@main_sessions_required
def vote(request, code):
    # initial flow  
    context = dict()
    context['code'] = code
    
    # main flow
    if request.method == 'GET':
        context['admin'] = request.session['main']['admin']
        context['themes'] = Room.objects.get(code=code).themes.filter(active=True)
        context['questions_for_ranking'] = get_best_questions(context['themes'])
        context['questions_for_vote'] = select_questions(request, context['themes'])
        
        
    elif request.method == 'POST':
        register_vote(request, code)
        return redirect('vote', code)
    
    # end flow
    context['selected'] = get_last_voted_theme(request.session['main']['voted_questions'])

    return render(request, f'{BP}/vote.html', context)



@main_sessions_required
def records_view(request, code):
    # initial flow   
    context = dict()
    context['code'] = code
    context['themes'] = Room.objects.get(code=code).themes.filter(active=False)
    
    # main flow
    context['answered'] = get_questions_answered(context['themes'])
    context['questions_for_ranking'] = get_questions_for_end_rank(context['themes'])
    context['admin'] = request.session['main']['admin']
    
    return render(request, f'{BP}/records.html', context)



@main_sessions_required
def settings_view(request, code):
    # initial flow
    context = dict()
    context['code'] = code
    context['room'] = Room.objects.get(code=code)
    context['total_of_questions'] = get_total_of_questions(context['room'])
    
    # main flow
    if request.method == 'POST':
        process = verify_process__settings(request)
        if process['action'] == 'create theme':
            create_theme(request, code)
        elif process['action'] == 'disable theme':
            disable_theme(request, code)
        elif process['action'] == 'update for admin':
            try_update_for_admin(request, code)
        
        return redirect('settings', code)
        
            
    # end flow
    context['admin'] = request.session['main']['admin']
    context['active_themes'] = context['room'].themes.filter(active=True).only('name')
    context['disabled_themes'] = context['room'].themes.filter(active=False).only('name')     
    
    return render(request, f'{BP}/settings.html', context)


