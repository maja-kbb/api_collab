from rest_framework import serializers
from .models import Osoba, Wpis, User, Ustawienia, Profil
from django.core.validators import FileExtensionValidator

class OsobaSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    imie = serializers.CharField(max_length = 50)  
    nazwisko = serializers.CharField(max_length = 50)
    email = serializers.EmailField(max_length=254)
    data_rejestracji = serializers.DateTimeField()

    def validate_imie(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Pole 'imie' moze zawierac tylko litery")
        return value
    
    def validate_nazwisko(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Pole 'nazwisko' moze zawierac tylko litery")
        return value

    def create(self, validated_data):
        return Osoba.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.imie = validated_data.get('imie', instance.imie)
        instance.nazwisko = validated_data.get('nazwisko', instance.nazwisko)
        instance.email = validated_data.get('email', instance.email)
        instance.data_rejestracji = validated_data.get('data_rejestracji', instance.data_rejestracji)
        instance.save()
        return instance





class WpisSerializer(serializers.Serializer):
    autor = serializers.PrimaryKeyRelatedField(queryset=Osoba.objects.all())
    tytul = serializers.CharField(max_length=100)
    tresc = serializers.CharField()
    data_utworzenia = serializers.DateTimeField()
    data_aktualizacji = serializers.DateTimeField()
    upl_img = serializers.ImageField()



    def create(self, validated_data):
        return Wpis.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.autor = validated_data.get('autor', instance.autor)
        instance.tytul = validated_data.get('tytul', instance.tytul)
        instance.tresc = validated_data.get('tresc', instance.tresc)
        instance.data_utworzenia = validated_data.get('data_utworzenia', instance.data_utworzenia)
        instance.data_aktualizacji = validated_data.get('data_aktualizacji', instance.data_aktualizacji)
        instance.upl_img = validated_data.get('upl_img', instance.upl_img)
        instance.upl_mov = validated_data.get('upl_mov', instance.upl_mov)
        instance.save()
        return instance


class ProfilSerializer(serializers.Serializer):
    osoba = serializers.PrimaryKeyRelatedField(queryset=Osoba.objects.all()) 
    data_urodzenia = serializers.DateField()
    telefon = serializers.CharField(max_length=15)
    avatar = serializers.ImageField()
    biografia = serializers.CharField()    

    
    
    
    def create(self, validated_data):
        return Profil.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.osoba = validated_data.get('osoba', instance.osoba)
        instance.data_urodzenia = validated_data.get('data_urodzenia', instance.data_urodzenia)
        instance.telefon = validated_data.get('telefon', instance.telefon)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.biografia= validated_data.get('biografia', instance.biografia)
        instance.save()
        return instance

    #def validate_telefon(self, value):
       # if not value.isdigit():
        #   raise serializers.ValidationError("Pole 'telefon' moze zawierac tylko cyfry")
        #return value

class UstawieniaSerializer(serializers.Serializer):
    osoba = serializers.PrimaryKeyRelatedField(queryset=Osoba.objects.all())
    motyw_kolor = serializers.CharField(max_length=10,default='light')
  

    def create(self, validated_data):
        osoba = self.context['request'].user.osoba
        return Ustawienia.objects.create(osoba=osoba, **validated_data)
    
    def update(self, instance, validated_data):
        instance.osoba = validated_data.get('osoba', instance.osoba)
        instance.motyw_kolor = validated_data.get('motyw_kolor', instance.motyw_kolor)
        instance.save()
        return instance