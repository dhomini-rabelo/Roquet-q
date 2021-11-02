from django.contrib import messages



def send_errors_of_asks(request, errors):
    if isinstance(errors, str):
        return messages.error(request, errors)    
    for field, error_message in errors.items():
        message_name = {'username': 'O username', 'question': 'A pergunta', 'theme': 'O tema'}
        messages.error(request, error_message.replace('Este campo', message_name[field]))
            
            
            
def user_permission(request, code):
    user_data = request.session.get('main')
    saved_code = request.session.get('code')
    
    if (user_data is None) or (saved_code is None):
        return False
    elif int(saved_code) != code:
        return False
    else:
        return True
