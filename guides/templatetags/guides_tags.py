import datetime

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def stalecheck(time):

    try:
        dt = datetime.datetime.strptime(time, "%Y/%m/%d")
    except ValueError:
        return mark_safe('<span class="alert alert-danger">unparsable</span>')

    days = abs ( (datetime.datetime.now() - dt).days )
    if days > 60:
        return mark_safe('<span class="alert alert-warning">stale</span>')
    else:
        return ""
