from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseForbidden
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Osoba, Profil, Wpis, Ustawienia
from .serializers import OsobaSerializer, ProfilSerializer, WpisSerializer, UstawieniaSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView
from django.contrib.auth.decorators import permission_required, login_required
from . import views
from .forms import DodajWpis

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


@login_required
def profil_user(request):
    osoba = Osoba.objects.get(user=request.user)
    profil = Profil.objects.get(osoba=osoba)
    return render(request, 'journal_app/profil_user.html', {'osoba': osoba, 'profil': profil})


@login_required
def home_page(request):
    osoba = Osoba.objects.get(user=request.user)
    profil = Profil.objects.get(osoba=osoba)
    wpisy = Wpis.objects.filter(autor = osoba)
    return render(request, 'journal_app/home_page.html', {'osoba': osoba, 'profil':profil, 'wpisy':wpisy})



def dodaj_wpis(request):
    if request.method == 'POST':
        form = DodajWpis(request.POST, request.FILES)
        if form.is_valid():
            osoba = Osoba.objects.get(user=request.user)
            wpis = form.save(commit=False)
            wpis.autor = osoba  
            wpis.save()
            return redirect('home-page')  
    else:
        form = DodajWpis()
    return render(request, 'journal_app/dodaj_wpis.html', {'form': form})


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


        



@permission_required('journal_app.view_osoba', raise_exception=True)
def osoba_view(request):
    if request.user.has_perm('journal_app.can_view_other_persons'):
        osoby = Osoba.objects.exclude(owner=request.user)
    else:
        osoby = Osoba.objects.filter(owner=request.user)

    return render(request, 'osoba_list.html', {'osoby': osoby})

