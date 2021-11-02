# django
from django.core.validators import validate_slug, validate_unicode_slug 
# this module
from .validators import validate_for_email, validate_unique, validate_caracters
from .utils import get_type
from .support import type_validation, adapt_form_errors
from .checks import check_null
# others
from string import digits
from decimal import Decimal
from datetime import datetime


def convert_validation(obj, new_type: str):
    if new_type == 'pass': return 'valid'
    initial_type = get_type(obj)
    type_validation(initial_type, new_type)
    if initial_type == 'str':
        if new_type == 'str': 
            return 'valid'
        elif new_type == 'int':
            try: 
                return int(obj)
            except:
                return 'convert_error'
        elif new_type == 'float':
            try: 
                return float(obj)
            except:
                return 'convert_error'
        elif new_type == 'decimal':
            try: 
                return Decimal(obj)
            except:
                return 'convert_error'
        elif new_type == 'bool':
            try:
                return bool(obj)
            except:
                return 'convert_error'
        elif new_type == 'date':
            try:
                date_check = datetime.strptime(obj, '%Y-%m-%d').date()
                return obj
            except:
                return 'convert_error'
        elif new_type == 'slug':
            try:
                validate_slug(obj)
                validate_unicode_slug(obj)
                return obj
            except:
                return 'convert_error'        
        elif new_type == 'email':
            condition = validate_for_email(obj)
            return obj if condition else 'convert_error'
    elif initial_type is None:
        return 'initial_type_error'
      
        
def get_post_form_errors(fields: list, Model=None):
    """
    Model list fields
    [[fields(example: name), variable_for_convert_validation, name_field_for_error_messages,
    specific_list_validation_with_tuples(example)[('unique', 'argument: slug')]
    ],]
    variable_for_convert_validation = 'pass' if field don't return str field
    """
    invalid_fields = []
    none_fields = []
    other_errors = []
    possible_types = ['str', 'int', 'decimal', 'bool', 'date',
                      'email', 'float', 'NoneType', 'slug']
    types_more_validations = ['unique', 'email', 'caracters', 'min-max-equal(length)']
    
    for field, convert_var, name, more_validations in fields:
        validation = convert_validation(field, convert_var)
        if str(validation) == 'initial_type_error' or check_null(field):
            none_fields.append(name)  
        elif str(validation) == 'convert_error':
            invalid_fields.append(name)
        else:
            for other_validation in more_validations:
                if other_validation[0] == 'unique':
                    field_ = int(field) if convert_var == 'int' else field
                    if not validate_unique(Model, other_validation[1], field_):
                        other_errors.append(['unique', name])
                if other_validation[0] == 'exists':
                    field_ = int(field) if convert_var == 'int' else field
                    if validate_unique(Model, other_validation[1], field_):
                        other_errors.append(['exists', name])
                if other_validation[0] == 'email':
                    if not validate_for_email(field):
                        other_errors.append(['email', name])
                if other_validation[0] == 'caracters':
                    if not validate_caracters(field, other_validation[1], other_validation[2]):
                        other_errors.append(['caracters', name])
                if other_validation[0] == 'min_length':
                    if len(str(field)) < other_validation[1]:
                        other_errors.append(['min_length', name, other_validation[1]])
                elif other_validation[0] == 'equal_length':
                    if len(str(field)) != other_validation[1]:
                        other_errors.append(['equal_length', name, other_validation[1]])
                if other_validation[0] == 'max_length':
                    if len(str(field)) > other_validation[1]:
                        other_errors.append(['max_length', name, other_validation[1]])
                if other_validation[0] == 'only_str':
                    if not validate_caracters(field, True, True, False, False):
                        other_errors.append(['caracters', name])

    
    form_errors = {'invalid_fields': invalid_fields, 'none_fields': none_fields,
                    'other_errors': other_errors}
    
    form_errors = adapt_form_errors(form_errors)
    return form_errors if form_errors != {} else None
    
    
def get_password_error(password, confirm_password):
    if not password == confirm_password:
        return 'As senhas nonvas senhas não são iguais'
    elif not validate_caracters(password, False, False):
        return 'A senha possui caracteres inválidos'
    elif len(password) < 8:
        return 'A senha é muito curta'
    return None


def change_password(user, current_password, new_password, new_password_confirm):
    errors_list = list()
    if current_password is None:
        errors_list.append('O campo senha atual não foi informado')
    if new_password is None:
        errors_list.append('O campo de nova senha não foi informado')
    if new_password_confirm is None:
        errors_list.append('O campo de confirmação de nova senha não foi informado')
    if errors_list == []:
        if not user.check_password(current_password):
            errors_list.append('A senha atual não está correta')
        else:
            error_password = get_password_error(new_password, new_password_confirm)
            if error_password is None:
                user.set_password(new_password)
                user.save()
            errors_list.append(error_password)
    return errors_list if errors_list != [] else None
    



class Session:
    def __init__(self, request, name, initial_value):
        self.name = name
        self.request = request
        self.edit(initial_value)
        self.value = request[name]
    
    def edit(self, value):
        self.request[self.name] = value
        
    def delete(self):
        self.request[self.name] = None