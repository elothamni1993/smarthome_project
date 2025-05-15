from django import template

register = template.Library()

@register.filter
def display_room(value):
    """Transforme 'living_room' en 'Living Room'."""
    return value.replace('_', ' ').title()
template.base.builtins.append(register)