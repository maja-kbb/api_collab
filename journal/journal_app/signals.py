from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Osoba, Profil

@receiver(post_save, sender=User)
def create_osoba_and_profil(sender, instance, created, **kwargs):
    if created:
        osoba = Osoba.objects.create(
            user=instance,
            imie=instance.first_name,
            nazwisko=instance.last_name,
            email=instance.email
        )
        Profil.objects.create(osoba=osoba)
