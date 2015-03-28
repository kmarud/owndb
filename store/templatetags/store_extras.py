from django import template
from django.db.models import Q

register = template.Library()


@register.filter
def instance(queryset, forminstance):
    o = queryset.get(Q(forminstance=forminstance) | Q(forminstance__isnull=True))
    return o.data