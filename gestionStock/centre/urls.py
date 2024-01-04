
# centre1/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from .views import ProduitVenteChart,chart_view,TopCustomerChart,chart_view2,EmployeManagementView, AbsenceChartAPIView,absence_create,paiement



urlpatterns = [
    path('sales/', views.record_sale, name='record_sale'),
    path('liste_ventes/', views.afficher_ventes,name='afficher_vente'),
    path('liste_ventes/', views.vente,name='montant'),
    path('api/produit-vente-chart/', ProduitVenteChart.as_view(), name='produit-vente-chart'),
    path('dashboard/', chart_view, name='chart1-view'),
    path('api/top-customer-chart/', TopCustomerChart.as_view(), name='top-customer-chart'),
    path('clientchart/', chart_view2, name='chart2-view'),
    path('employe-management/', EmployeManagementView.as_view(), name='employe-management'),
    path('api/absence-chart/', AbsenceChartAPIView.as_view(), name='absence-chart-api'),
    path('absence/', views.absence_create,name='absence'),
    path('avance/', views.paiement, name='paiement'),
]
