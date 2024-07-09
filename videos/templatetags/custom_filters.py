from django import template

register = template.Library()


@register.filter
def gender_to_avatar(gender):
    value = 13 if gender == "Male" else 16
    return value
