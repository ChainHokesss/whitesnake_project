from django.dispatch import receiver
from django.db.models.signals import post_save

from src.customers.models import CustomerModel
from src.core.models import BaseUser


@receiver(post_save, sender=BaseUser)
def update_customer_signal(sender, instance, created, **kwargs):
    if created:
        CustomerModel.objects.create(user=instance)
    instance.customermodel.save()
