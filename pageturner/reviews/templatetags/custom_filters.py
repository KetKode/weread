import random

from django import template

register = template.Library()


@register.filter(name='random_color')
def random_color(value):
    r = random.randint(128, 255)  # Red component (128-255)
    g = random.randint(0, 64)  # Green component (0-64, kept low for purple shades)
    b = random.randint(128, 255)  # Blue component (128-255)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)
