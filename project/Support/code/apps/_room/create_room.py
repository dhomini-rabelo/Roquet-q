from Support.code.core import get_post_form_errors
from Support.code.validators import validate_unique
from Support.code.utils import filters
from room.models import Room
from random import randint
import hashlib


def get_room_code():
    code = randint(100000, 999999)
    while not validate_unique(Room, 'code', code):
        code = randint(100000, 999999)
    return code


def create_an_room(request):
    rp = request.POST
    
    username, password, code = filters(rp.get('username')), filters(rp.get('password')), rp.get('code') 

    fv = [
        [username, 'str', 'username', [('max_length', 128)]],
        [password, 'str', 'password', [('caracters', True, True), ('min_length', 4), ('max_length', 128)]],
        [code, 'int', 'code', [('unique', 'code'), ('equal_length', 6)]],
    ]  # form validation
    
    form_errors = get_post_form_errors(fv, Room)
    
    if form_errors is None:
        encrypted_password = hashlib.md5(password.encode()).hexdigest()
        new_room = Room.objects.create(creator=username, code=code, password_admin=encrypted_password)
        new_room.save()
        return {'status': 'success'}
    else:
        return {'status': 'error', 'errors': form_errors}

