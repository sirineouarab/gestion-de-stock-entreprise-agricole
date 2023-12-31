
# centre1/urls.py
from django.urls import path
from . import views
from .views import Dashboard

urlpatterns = [
    path('sales/', views.record_sale, name='record_sale'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('liste_ventes/', views.afficher_ventes,name='afficher_vente'),
    # Ajouter d'autres patterns d'URL au besoin
]
