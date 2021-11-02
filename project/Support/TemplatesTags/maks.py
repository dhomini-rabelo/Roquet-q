from django import template


register = template.Library()


@register.filter(name='br_money')
def _br_money(value):
    integer_value = str(value)[:-3]
    size = len(integer_value)
    representation = []
    count = 0
    for c in range(size-1, -1, -1):
        count += 1
        if count % 3 == 0 and count != size:
            representation.append(integer_value[c])
            representation.append('.')
        else:
            representation.append(integer_value[c])
    return ''.join(representation)[::-1] + f',{str(value)[-2:]}'


@register.filter(name='cpf')
def _cpf(value):
    list_cpf = list(value)
    list_cpf.insert(3, '.')
    list_cpf.insert(7, '.')
    list_cpf.insert(11, '-')
    return "".join(list_cpf)


@register.filter(name='card')
def _card(value):
    list_card = list(value)
    list_card.insert(4, ' ')
    list_card.insert(9, ' ')
    list_card.insert(14, ' ')
    return "".join(list_card)    


@register.filter(name='phone_br')
def _phone_br(value):
    list_phone = list(value)
    list_phone.insert(0, '(')
    list_phone.insert(3, ') ')
    list_phone.insert(9, '-')
    return "".join(list_phone) 


@register.filter(name='cnpj')
def _cnpj(value):
    list_cnpj = list(value)
    list_cnpj.insert(2, '.')
    list_cnpj.insert(6, '.')
    list_cnpj.insert(10, '/')
    list_cnpj.insert(15, '-')
    return "".join(list_cnpj)