from django import template

register = template.Library()

@register.filter
def to_range(value):
    return range(int(value))

@register.filter
def us_date(value):
    return "{d.year}-{d.month}-{d.day} {d.hour}:{d.minute}".format(d=value)
