from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name='enumerate')
def _enumerate(iterable):
    return enumerate(iterable)


@register.filter(name='next')
def _next(obj):
    return next(obj)


@register.filter(name='get_item')
def _get_item(obj, index_):
    return obj[index_]


@register.filter(name='str')
def _str(obj):
    return str(obj)


@register.filter(name='slice')
def _slice(obj, index_):
    if len(obj) >= index_:
        return obj[:index_]
    else:
        return obj
    
    
@register.filter(name='horary')
def _horary(question):
    horary = question.creation - timedelta(hours=3)
    return horary.strftime('%H:%M')


@register.filter(name='theme')
def _theme(question):
    name_theme = question.theme.name
    return name_theme
