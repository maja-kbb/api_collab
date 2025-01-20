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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import OsobaSerializer
from rest_framework.generics import ListAPIView
from .models import Osoba
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from .models import Stanowisko, Osoba

class OsobaCreateView(APIView):
    def post(self, request):
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(właściciel=request.user)  # Dodanie właściciela
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OsobaUpdateView(UpdateAPIView):
    queryset = Osoba.objects.all()
    serializer_class = OsobaSerializer
    permission_classes = [IsAuthenticated]

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OsobaSerializer

class OsobaDeleteView(DestroyAPIView):
    queryset = Osoba.objects.all()
    permission_classes = [IsAuthenticated]

class StanowiskoMembersView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({"message": "Hello, authenticated user!"})
    
    def get_queryset(self):
        return Osoba.objects.filter(właściciel=self.request.user)
        return super().get_queryset().filter(właściciel=self.request.user)

    def get(self, request, stanowisko_id):
        try:
            stanowisko = Stanowisko.objects.get(pk=stanowisko_id)
            members = stanowisko.osoby_set.all()
            serializer = OsobaSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Stanowisko.DoesNotExist:
            return Response({"error": "Stanowisko not found"}, status=status.HTTP_404_NOT_FOUND)
        
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.urls import path
from . import views


@permission_required('app_name.view_osoba', raise_exception=True)
def osoba_view(request):
    # Twoja logika widoku
    return render(request, 'osoba_list.html')
    if request.user.has_perm('app_name.can_view_other_persons'):
        osoby = Osoba.objects.exclude(owner=request.user)
    else:
        osoby = Osoba.objects.filter(owner=request.user)

    return render(request, 'osoba_list.html', {'osoby': osoby})

