from django import template
from django.utils import timezone
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def first_word(value):
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
    elif months > 0:
        return f"{months} meses" if months > 1 else "1 mês"
    elif days > 0:
        return f"{days} dias" if days > 1 else "1 dia"
    elif seconds // 3600 > 0:
        hours = seconds // 3600
        return f"{hours} horas" if hours > 1 else "1 hora"
    elif seconds // 60 > 0:
        minutes = seconds // 60
        return f"{minutes} minutos" if minutes > 1 else "1 minuto"
    else:
        return f"{seconds} segundos" if seconds > 1 else "1 segundo"
