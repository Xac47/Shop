from django import template

from subscribe_email.forms import SubscribeEmailForm

register = template.Library()


@register.simple_tag
def get_form_subscribe_email():
    return SubscribeEmailForm()
