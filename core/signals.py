from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth.models import User
from core.models import Customer
 

@receiver(signals.post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.get_or_create(user=instance)