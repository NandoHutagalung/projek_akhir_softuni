from django import template

register = template.Library()

@register.filter
def rupiah(value):
    try:
        return "Rp {:,}".format(value).replace(",", ".")
    except ValueError:
        return value
