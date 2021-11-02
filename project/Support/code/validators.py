# django
from django.core.validators import validate_email
# others
from string import ascii_letters, digits


def validate_caracters(text: str, with_accents=True, spaces=True, use_symbols=True, use_numbers=True):
    accents = 'áàéèíìóòúùâêîôûãõ' if with_accents else ''
    space = ' ' if spaces else ''
    symbols = "@.+-_" if use_symbols else ''
    numbers = digits if use_numbers else ''
    alloweds = symbols + numbers + ascii_letters + accents + space
    for letter in text.lower():
       if letter not in alloweds:
           return False
    return True


def validate_for_email(email: str):
    try:
        validate_email(email)
        return True
    except:
        return False
    
    
def validate_unique(Model, field: str, new_field):
    fields = list(item[0] for item in Model.objects.values_list(field))
    if new_field in fields:
        return False
    return True
    


    