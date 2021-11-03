from django.contrib import messages
from urllib.parse import quote


def send_errors_of_room(request, errors: dict):
    for field, error_message in errors.items():
        if error_message == 'Já está em uso':
            messages.error(request, 'código já esta em uso')
            continue
        message_name = {'username': 'O username', 'password': 'A senha', 'code': 'O código', 'theme': 'O tema'}
        messages.error(request, error_message.replace('Este campo', message_name[field]))
        
        
def get_username_for_url(request):
    username = request.POST.get('username')
    if username is None:
        return ''
    elif username.strip() == '':
        return ''
    adapted_username_for_url = quote(username)
    return f'?username={adapted_username_for_url}'