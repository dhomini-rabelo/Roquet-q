from django.db.models import F


def get_questions_answered(themes):
    response = {}
    
    for theme in themes:
        response[theme.name] = theme.questions.filter(answered=True).order_by('creation')
        
    return response
        

def get_questions_for_end_rank(themes):
    questions = {}

    for theme in themes:
        questions[theme.name] = theme.questions.annotate(score=F('up_votes')-F('down_votes')).order_by('-score', '-up_votes')
        
    return questions