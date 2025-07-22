from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Offer
import os


@receiver(post_delete, sender=Offer)
def delete_offer_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)