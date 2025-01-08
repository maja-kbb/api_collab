from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Osoba, Profil, Wpis, Ustawienia
from .serializers import OsobaSerializer, ProfilSerializer, WpisSerializer, UstawieniaSerializer
# Create your views here.

@api_view(['GET'])
def osoba_list(request):
    """
    Lista wszystkich obiektów modelu Osoba.
    """
    if request.method == 'GET':
        osoby = Osoba.objects.all()
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)





@api_view(['GET', 'PUT', 'DELETE'])
def osoba_detail(request, pk):


    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Szczegóły pojedynczego obiektu Osoba.
    """
    if request.method == 'GET':
        osoba = Osoba.objects.get(pk=pk)
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OsobaSerializer(osoba, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def osoba_filter(request, substring):
    osoby = Osoba.objects.filter(imie__icontains=substring) | Osoba.objects.filter(nazwisko__icontains=substring)
    serializer = OsobaSerializer(osoby, many=True)
    return Response(serializer.data)



def osoba_list_html(request):
    osoby = Osoba.objects.all()
    return render(request,
                  "journal_app/osoba/list.html",
                  {'osoby': osoby})


def osoba_detail_html(request, id):
    # pobieramy konkretny obiekt Person
    try:
        osoba = Osoba.objects.get(id=id)
    except Osoba.DoesNotExist:
        raise Http404("Obiekt Osoba o podanym id nie istnieje")

    return render(request,
                  "journal_app/osoba/detail.html",
                  {'osoba': osoba})