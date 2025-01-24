from django import forms
from .models import Wpis, Profil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DodajWpis(forms.ModelForm):
    class Meta:
        model = Wpis
        fields = ['tytul', 'tresc','upl_img']  
        widgets = {
            'tytul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tytuł wpisu'}),
            'tresc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Treść wpisu'}),
        }
    



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Twój email'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten e-mail jest już zajęty.")
        return email



class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['data_urodzenia', 'telefon', 'biografia', 'avatar']  

    def __init__(self, *args, **kwargs):
        super(ProfilForm, self).__init__(*args, **kwargs)