from django.shortcuts import render, redirect
from Support.code.apps._asks.decorators import main_sessions_required
from Support.code.apps._asks.settings import verify_process__settings, create_theme, try_update_for_admin, disable_theme, get_total_of_questions
from Support.code.apps._asks.ask import delete_question
from Support.code.apps import generate_key
from room.models import Room, Theme
from django.contrib import messages



BP = 'apps/asks' # base path


@main_sessions_required
def ask(request, code):
    if request.method == 'GET':
        context = dict()
        context['code'] = code
        context['username'] = request.session['main']['username']
        context['themes'] = Room.objects.get(code=code).themes.filter(active=True)
        context['page'] = request.GET.get('p') if request.GET.get('p') else '1'

    elif request.method == 'POST':
        delete_question(request, code)
        page = request.POST.get('page') if request.POST.get('page') else '1'
        return redirect(f'/{code}/perguntar?p={page}')
    
    return render(request, f'{BP}/ask.html', context)



@main_sessions_required
def vote(request, code):
    context = dict()
    context['code'] = code
    context['username'] = request.session['main']['username']
    context['admin'] = request.session['main']['admin']
    context['themes'] = Room.objects.get(code=code).themes.filter(active=True)
    context['user_key'] = request.session['user_key']
    context['admin_key'] = request.session.get('admin_key')
    messages.warning(request, 'Espere as perguntas carregarem para selecionar o tema')

    return render(request, f'{BP}/vote.html', context)



@main_sessions_required
def records_view(request, code):
    # initial flow   
    context = dict()
    context['code'] = code
    context['themes'] = Room.objects.get(code=code).themes.filter(active=False)
    context['admin'] = request.session['main']['admin']
    messages.warning(request, 'Espere as perguntas carregarem para selecionar o tema')
    
    return render(request, f'{BP}/records.html', context)



@main_sessions_required
def settings_view(request, code):
    # initial flow
    if request.method == 'GET':
        context = dict()
        context['code'] = code
        context['room'] = Room.objects.get(code=code)
        context['admin'] = request.session['main']['admin']
        
    # main flow
    elif request.method == 'POST':
        process = verify_process__settings(request)
        if process['action'] == 'create theme':
            create_theme(request, code)
        elif process['action'] == 'disable theme':
            disable_theme(request, code)
        elif process['action'] == 'update for admin':
            try_update_for_admin(request, code)
        
        return redirect('settings', code)
        
            
    return render(request, f'{BP}/settings.html', context)
