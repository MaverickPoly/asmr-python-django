from django import template
from django.contrib.auth import get_user_model
from accounts.models import Account

register = template.Library()

@register.filter(name='get_user_account')
def get_user_account(user):
    """
    Returns the Account object associated with the current user
    Usage: {{ request.user|get_user_account }}
    """
    if not user.is_authenticated:
        return None
    try:
        return Account.objects.get(user=user)
    except Account.DoesNotExist:
        return None