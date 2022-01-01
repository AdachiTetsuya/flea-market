from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from allauth.account.models import EmailAddress

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    old_email = EmailAddress.objects.filter(user=user).exclude(email=email_address.email)
    if old_email.exists():
        user.email = email_address.email
        user.save()
        email_address.primary = True
        email_address.save()
        old_email.delete()
    else:
        pass