from random import randint, shuffle
from Support.code.utils import filters
from asks.models import Question
from room.models import Room
from django.db.models import Q, F

# support functions

def save_questions_for_vote(questions: dict):
    for theme_name, set_of_questions in questions.items():
        questions[theme_name] = [question.id for question in set_of_questions]
    return questions


def get_questions(request, theme):
    my_questions = [question['text'] for question in request.session['main']['my_questions']]
    if my_questions != []:
        function = lambda theme: {theme.name : theme.questions.exclude(Q(text__in=my_questions) | Q(answered=True))}
    else:
        function = lambda theme: {theme.name : theme.questions.exclude(answered=True)}
        
    return function(theme)


def select_items(query_set, quantity=3):
    if len(query_set) <= quantity:
        return list(query_set)
    
    selecteds = []
    
    while len(selecteds) < quantity:
        selected = randint(0, len(query_set) - 1)
        if selected not in selecteds:
            selecteds.append(selected)
    
    return [query_set[number] for number in selecteds]
        
        
        
def get_question(request, theme, id_list: list):
    questions = get_questions(request, theme)
    
    for question in questions[theme.name]:
        if question.id not in (request.session['main']['voted_questions'] + id_list):
            return question
    
    return None


def get_questions_by_id(request):
    saved_questions = request.session['main']['questions_saved_to_vote'].copy()
    code = request.session['code']
    
    themes = Room.objects.get(code=code).themes.all()
    
    for theme_name, id_questions in saved_questions.copy().items():
        questions = []
        theme = themes.get(name=theme_name)
        if theme.active == True:
            for id in id_questions:
                question = Question.objects.get(id=id)
                if id not in request.session['main']['voted_questions']:
                    questions.append(question)
                else:
                    new_id_questions = id_questions[:]
                    new_id_questions.remove(id)
                    new_question = get_question(request, theme, id_questions)
                    if new_question is not None:
                        questions.append(new_question)
                        new_id_questions.append(new_question.id)
                    
                    request.session['main']['questions_saved_to_vote'][theme_name] = new_id_questions

                    
            saved_questions[theme_name] = questions
        else:
            del saved_questions[theme_name]            
            del request.session['main']['questions_saved_to_vote'][theme_name]
    
    return saved_questions


def regulate_sets(request, sets_of_questions: dict, themes):
    regulated_sets = dict()
        
    if not len(sets_of_questions.keys()) == len(themes):
        for theme in themes:
            if theme.name not in sets_of_questions.keys():
                new_questions = get_questions(request, theme)
                regulated_sets[theme.name] = select_items(new_questions[theme.name], 5)
    
    if regulated_sets != {}:
        new_questions_of_theme = save_questions_for_vote(regulated_sets.copy())
        request.session['main']['questions_saved_to_vote'] = request.session['main']['questions_saved_to_vote'] | new_questions_of_theme
        

    return sets_of_questions | regulated_sets
            



# main functions

def select_questions(request, themes):
    if request.session['main'].get('questions_saved_to_vote') is None:
        sets_of_questions = [get_questions(request, theme) for theme in themes]
        
        super_set = dict()
        for set_questions in sets_of_questions: 
            super_set = super_set | set_questions
            

        for theme_name, set_questions in super_set.items():                            
            super_set[theme_name] = select_items(set_questions, 5)

        request.session['main']['questions_saved_to_vote'] = save_questions_for_vote(super_set.copy())
        print(super_set)
        return super_set
    else:
        sets_of_questions = get_questions_by_id(request)
        sets_of_questions = regulate_sets(request, sets_of_questions, themes)
        return sets_of_questions     
    
    
def register_vote(request, code):
    # main flow
    rp = request.POST
    text, theme, action = filters(rp.get('text')), filters(rp.get('theme')), filters(rp.get('action'))
    
    room = Room.objects.get(code=code)
    theme_of_room = room.themes.get(name=theme)
    question = theme_of_room.questions.filter(text=text).first()
    
    if question is None: # case question was deleted
        request.session['main']['voted_questions'].append(question.id)
        return 
     
    
    if action == 'up' and question.id not in request.session['main']['voted_questions']:
        question.up_votes += 1
    elif action == 'down' and question.id not in request.session['main']['voted_questions']:
        question.down_votes += 1
    elif action == 'mark' and request.session['main']['admin']:
        question.answered = True
    
    
    question.save()
    
    # end flow
    request.session['main']['voted_questions'].append(question.id)
    
        
        
def get_best_questions(themes):
    best_questions = {}
    
    for theme in themes:
        questions = theme.questions.filter(answered=False).annotate(score=F('up_votes')-F('down_votes')).order_by('-score')
        if questions.count() >= 5:
            best_questions[theme.name] = questions[:5]
        else:
            best_questions[theme.name] = questions
            
    return best_questions
        
        
    

def get_last_voted_theme(voted_questions: list):
    if len(voted_questions) != 0:
        id_last_voted_question = voted_questions[-1]
        last_voted_question = Question.objects.filter(id=id_last_voted_question).first()
        if last_voted_question is not None:
            return last_voted_question.theme.name
        else:
            return 'none'
    else:
        return 'none'