from django import template
from django.db.models import Q

register = template.Library()


@register.filter
def instance(queryset, forminstance):
    o = queryset.get(Q(forminstance=forminstance) | Q(forminstance__isnull=True))
    return o.data
    
@register.filter
def split_all(value, splitter='|'):
    value = value.split(splitter)
    return value
    
@register.filter
def split_remove_first(value, splitter='|'):
    value = value.split(splitter)
    del value[0]
    return value
    