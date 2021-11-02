# django
from django.contrib import auth
# others
from decimal import Decimal
from datetime import datetime
    
    
def check_null(obj):
    try:
        if obj is None:
            return True
        elif isinstance(obj, str) and obj.strip() == '':
            return True
        elif len(obj) == 0:
            return True
    except TypeError:
        pass
    return False


def checks_null(input_list: list):
    for item in input_list:
        try:
            if item is None:
                return True
            elif isinstance(item, str) and item.strip() == '':
                return True
            elif len(item) == 0:
                return True
            elif len(list(item)) == 0:
                return True
        except TypeError:
            pass
    return False


def check_is_logged(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        return True
    return False
