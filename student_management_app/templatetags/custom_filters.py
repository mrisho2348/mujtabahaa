from django import template
register = template.Library()

@register.filter(name='strftime')
def strftime(date, format_string):
    return date.strftime(format_string)
