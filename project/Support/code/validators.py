# django
from django.core.validators import validate_email
# others
from string import ascii_letters, digits
from typing import Any

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
    
    
def validate_unique(Model, field_name: str, field: Any, use_queryset=True):
    model = Model.objects if not use_queryset else Model
    current_fields = model.values_list(field_name, flat=True)
    
    if field in current_fields:
        return False
    return True
    


    