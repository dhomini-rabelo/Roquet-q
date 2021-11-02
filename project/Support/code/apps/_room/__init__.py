from django.contrib import messages



def send_errors_of_room(request, errors: dict):
    for field, error_message in errors.items():
        if error_message == 'Já está em uso':
            messages.error(request, 'código já esta em uso')
            continue
        message_name = {'username': 'O username', 'password': 'A senha', 'code': 'O código', 'theme': 'O tema'}
        messages.error(request, error_message.replace('Este campo', message_name[field]))