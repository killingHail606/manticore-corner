from django import template

register = template.Library()


@register.filter
def status_is(books, status):
    return books.filter(status=status)
