from django.contrib import admin

# Register your models here
from .models import Osoba, Profil, Wpis, Ustawienia

admin.site.register(Osoba)
admin.site.register(Profil)
admin.site.register(Wpis)
admin.site.register(Ustawienia)


class OsobaAdmin(admin.ModelAdmin):
    readonly_fields = ['data_rejestracji']
    list_display = ('imie', 'nazwisko', 'email', 'data_rejestracji')
    list_filter = ('data_rejestracji')

