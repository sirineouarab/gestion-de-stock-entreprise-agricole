
# centre1/urls.py
from django.urls import path
from . import views

from .views import ProduitVenteChart,chart_view,TopCustomerChart,chart_view2


urlpatterns = [
    path('sales/', views.record_sale, name='record_sale'),
    
    path('liste_ventes/', views.afficher_ventes,name='afficher_vente'),
    path('liste_ventes/', views.vente,name='montant'),
    path('api/produit-vente-chart/', ProduitVenteChart.as_view(), name='produit-vente-chart'),
    path('dashboard/', chart_view, name='chart-view'),
    path('api/top-customer-chart/', TopCustomerChart.as_view(), name='top-customer-chart'),
   
    path('clientchart/', chart_view2, name='chart-view'),

    # Ajouter d'autres patterns d'URL au besoin
]
