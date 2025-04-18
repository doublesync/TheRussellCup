import markdown
from django import template

register = template.Library()


@register.filter
def convert_to_markdown(value):
    """
    Convert a string to markdown format.
    """

    return markdown.markdown(value, extensions=["markdown.extensions.fenced_code"])
