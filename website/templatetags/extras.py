from django import template
from datetime import datetime

register = template.Library()

@register.filter
def to_range(value):
    return range(int(value))

@register.filter
def us_date(value):
    return "{d.year}-{d.month}-{d.day} {d.hour}:{d.minute}".format(d=value)

@register.filter
def is_closed(value):
    return value < datetime.today()

@register.filter
def weekday(value):
    wkd = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    return wkd[value]
