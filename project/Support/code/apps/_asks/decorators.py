from . import user_permission
from django.shortcuts import redirect



def main_sessions_required(view_function):
    
    def verification(*args, **kwargs):
        if user_permission(*args, **kwargs):
            return view_function(*args, **kwargs)
        else:
            return redirect('enter_room')
    
    return verification