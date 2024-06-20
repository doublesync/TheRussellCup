# Django imports
from django import template

# Create your tags here.
register = template.Library()


# This is a custom template tag that will be used to style the form fields in the create_player.html template.
@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
