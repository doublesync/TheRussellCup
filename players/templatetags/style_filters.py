from django import template

import simulation.scripts.attribute as attribute
import simulation.scripts.badge as badge
import simulation.scripts.tendency as tendency

register = template.Library()


@register.filter
def stringify(number):
    """
    Converts a number to a string. If the number is an integer, it will be converted to a string.
    """

    return str(number)


@register.filter
def add_class(field, css):
    """
    "Adds a CSS class to a form field.
    """

    return field.as_widget(attrs={"class": css})


@register.filter
def add_attr(field, attr):
    """
    Adds an attribute to a form field.
    """

    return field.as_widget(attrs=attr)


@register.filter
def add_style(field, style):
    """
    Adds a style to a form field.
    """

    return field.as_widget(attrs={"style": style})


@register.filter
def add_attribute_color(attribute):
    """
    Adds a color to an attribute based on its value.
    """

    try:
        attribute = float(attribute)
    except (ValueError, TypeError):
        return "background-color: #212121; color: white;"

    if 55 < attribute < 70:
        return "background-color: #1d2e68; color: white;"
    elif 70 <= attribute < 80:
        return "background-color: #886300; color: white;"
    elif 80 <= attribute < 90:
        return "background-color: darkgreen; color: white;"
    elif attribute >= 90:
        return "background-color: #800080; color: white;"
    else:
        return "background-color: #212121; color: white;"


@register.filter
def add_badge_color(badge):
    """
    Adds a color to a badge based on its value.
    """

    badge_colors = {
        1: "background-color: #2b1700; color: white;",
        2: "background-color: #000000; color: white;",
        3: "background-color: #886300;",
        4: "background-color: #800080; color: white;",
        5: "background-color: #a52a2a; color: white;",
    }

    return badge_colors.get(badge, "background-color: #212121; color: white;")


@register.filter
def add_attribute_category(a):
    """
    Adds a category to an attribute based on its value.
    """

    a = a.replace("attribute_", "")
    for k, v in attribute.attribute_categories.items():
        if a in v:
            return k


@register.filter
def add_badge_category(b):
    """
    Adds a category to a badge based on its value.
    """

    for k, v in badge.badge_categories.items():
        if b in v:
            return k


@register.filter
def add_tendency_category(t):
    """
    Adds a category to a tendency based on its value.
    """

    for k, v in tendency.tendency_categories.items():
        if t in v:
            return k


@register.filter
def convert_position(p):
    """
    Converts a position abbreviation to its full name.
    """

    positions = {
        "PG": "Point Guard",
        "SG": "Shooting Guard",
        "SF": "Small Forward",
        "PF": "Power Forward",
        "C": "Center",
    }
    return positions.get(p, "Unknown Position")


@register.filter
def percentage(value, total):
    """
    Calculates the percentage of a value with respect to a total.
    """

    try:
        return (value / total) * 100
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def get_item(dictionary, key):
    """
    Retrieves an item from a dictionary using a key.
    """

    return dictionary.get(key)


@register.filter
def attr(obj, field_name):
    """
    Retrieves an attribute from an object using its name.
    """

    return getattr(obj, field_name, None)
