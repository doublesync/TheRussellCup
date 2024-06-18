# Django imports
from django import template

# Local imports
import markdown

register = template.Library()


@register.filter
def convert_to_markdown(value):
    return markdown.markdown(value, extensions=["markdown.extensions.fenced_code"])
