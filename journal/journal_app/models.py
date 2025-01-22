from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Create your models here
class Osoba(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='osoba')
    imie = models.CharField(max_length = 50)  # pole tekstowe
    nazwisko = models.CharField(max_length = 50)
    email = models.EmailField(max_length=254, unique=True)
    data_rejestracji = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.user})"
    
    class Meta:
        ordering = ["nazwisko"]
        verbose_name_plural = "Osoby"
        permissions = [
            ("view_other_person", "Moze zobaczyc osoby innych włascicieli"),
            
        ]
    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

    


class Profil(models.Model):
    osoba = models.OneToOneField(Osoba, on_delete=models.CASCADE, related_name='profil') #do polaczenia z modelem osoba
    data_urodzenia = models.DateField(null=True, blank=True)
    telefon = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    biografia = models.TextField(null=True, blank=True) #zeby mozna bylo jakis opis profilu sobie dodac

    def __str__(self):
        return f"Profil: {self.osoba.user}"
    




class Ustawienia(models.Model):
    osoba = models.OneToOneField(Osoba, on_delete=models.CASCADE, related_name='ustawienia')
    motyw_kolor = models.CharField(max_length=10, choices=[
        ('light', 'Jasny'),
        ('dark', 'Ciemny'),
    ], default='light')
    

    def __str__(self):
        return f"Ustawienia: {self.osoba.user}"
    



class Wpis(models.Model):
    autor = models.ForeignKey(Osoba, on_delete=models.CASCADE, related_name='wpisy')
    tytul = models.CharField(max_length=100)
    tresc = models.TextField()
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_aktualizacji = models.DateTimeField(auto_now=True)
    upl_img = models.ImageField(upload_to='imgs_uploaded', null = True, blank = True)

    def __str__(self):
        return f"Wpis: {self.tytul} ({self.autor.user})"

