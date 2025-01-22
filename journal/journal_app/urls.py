from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import OsobaUpdateView, OsobaDeleteView, ProtectedView

urlpatterns = [
    
    path('osoby/', views.osoba_list, name='osoba-list'),
    path('osoby/<int:pk>/', views.osoba_detail, name='osoba-detail'),
    path('osoby/filtrowane/<str:substring>/', views.osoba_filter, name='osoba-filter'),
    path('osoby_html/', views.osoba_list_html, name = 'osoba-list-html'),
    path('osoby_html/<int:id>/', views.osoba_detail_html, name = 'osoba-detail-html'),
    path('osoby/update/<int:pk>/', OsobaUpdateView.as_view(), name='osoba-update'),
    path('osoby/delete/<int:pk>/', OsobaDeleteView.as_view(), name='osoba-delete'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('login/', auth_views.LoginView.as_view(template_name='journal_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name ='journal_app/logout.html'), name='logout'),
    path('profil/', views.profil_user, name='profil-user'), 
    path('home/', views.home_page, name='home-page'),
    path('post/', views.dodaj_wpis, name='dodaj-wpis')

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)