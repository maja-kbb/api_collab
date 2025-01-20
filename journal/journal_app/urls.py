from django.urls import path, include
from . import views
from .views import ProtectedView
from .views import StanowiskoMembersView

urlpatterns = [
    
    path('osoby/', views.osoba_list, name='osoba-list'),
    path('osoby/<int:pk>/', views.osoba_detail, name='osoba-detail'),
    path('osoby/filtrowane/<str:substring>/', views.osoba_filter, name='osoba-filter'),
    path('osoby_html/', views.osoba_list_html, name = 'osoba-list-html'),
    path('osoby_html/<int:id>/', views.osoba_detail_html, name = 'osoba-detail-html'),
    path('osoby/update/<int:pk>/', views.osoba_update, name='osoba-update'),
    path('osoby/delete/<int:pk>/', views.osoba_delete, name='osoba-delete'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('stanowisko/<int:stanowisko_id>/members/', StanowiskoMembersView.as_view()),
]