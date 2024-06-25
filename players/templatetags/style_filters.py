# Django imports
from django import template

# Local imports
import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency

# Create your tags here.
register = template.Library()


# This is a custom template tag that will be used to style the form fields in the create_player.html template.
@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def add_attr(field, attr):
    return field.as_widget(attrs=attr)


@register.filter
def add_style(field, style):
    return field.as_widget(attrs={"style": style})


@register.filter
def add_attribute_color(attribute):
    if attribute < 70 and attribute > 55:
        return "background-color: #1d2e68"
    elif attribute >= 70 and attribute < 80:
        return "background-color: #886300"
    elif attribute >= 80 and attribute < 90:
        return "background-color: darkgreen"
    elif attribute >= 90:
        return "background-color: #800080"
    else:
        return "background-color: #212121"


@register.filter
def add_badge_color(badge):
    if badge == 1:
        return "background-color: #2b1700"
    elif badge == 2:
        return "background-color: #3b3b3b"
    elif badge == 3:
        return "background-color: #886300"
    elif badge == 4:
        return "background-color: #800080"
    else:
        return "background-color: #212121"


@register.filter
def add_attribute_category(a):
    a = a.replace("attribute_", "")
    for k, v in attribute.attribute_categories.items():
        if a in v:
            return k


@register.filter
def add_badge_category(b):
    for k, v in badge.badge_categories.items():
        if b in v:
            return k
        
@register.filter
def add_tendency_category(t):
    for k, v in tendency.tendency_categories.items():
        if t in v:
            return k


@register.filter
def convert_position(p):
    positions = {
        "PG": "Point Guard",
        "SG": "Shooting Guard",
        "SF": "Small Forward",
        "PF": "Power Forward",
        "C": "Center",
    }
    if p in positions:
        return positions[p]