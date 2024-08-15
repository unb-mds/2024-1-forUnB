""" Módulo com filtros customizados para templates. """

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def first_word(value):
    """ Retorna a primeira palavra de uma string. """
    return value.split(' ')[0]

@register.filter
def custom_timesince(value, now=None):
    """
    Retorna o tempo desde que o objeto foi criado, em português.
    """
    if not value:
        return ""

    delta = (now or timezone.now()) - value
    days = delta.days
    seconds = delta.seconds
    months = days // 30
    years = days // 365

    if years > 0:
        return f"{years} anos" if years > 1 else "1 ano"
    if months > 0:
        return f"{months} meses" if months > 1 else "1 mês"
    if days > 0:
        return f"{days} dias" if days > 1 else "1 dia"
    if seconds // 3600 > 0:
        hours = seconds // 3600
        return f"{hours} horas" if hours > 1 else "1 hora"
    if seconds // 60 > 0:
        minutes = seconds // 60
        return f"{minutes} minutos" if minutes > 1 else "1 minuto"
    return f"{seconds} segundos" if seconds > 1 else "1 segundo"
