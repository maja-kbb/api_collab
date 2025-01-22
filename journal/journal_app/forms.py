from django import forms
from .models import Wpis

class DodajWpis(forms.ModelForm):
    class Meta:
        model = Wpis
        fields = ['tytul', 'tresc','upl_img']  
        widgets = {
            'tytul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tytuł wpisu'}),
            'tresc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Treść wpisu'}),
        }
    