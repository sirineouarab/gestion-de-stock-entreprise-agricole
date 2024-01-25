
# centre1/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from .views import ProduitVenteChart,chart_view,TopCustomerChart,chart_view2,EmployeManagementView,add_reglement, AbsenceChartAPIView,absence_create,paiement,liste_employes,list_transferts_recu,calculate_total_and_benefit,get_client_credit,_transferts_,tablesManagement,deleteProduct,searchProduct,newProduct,editProduct,editClient,newClient,searchClient,deleteClient,deleteVente



urlpatterns = [
    path('sales/', views.record_sale, name='record_sale'),
    path('liste_ventes/', views.afficher_ventes,name='afficher_vente'),
    #path('liste_ventes/', views.vente,name='montant'),
    path('api/produit-vente-chart/', ProduitVenteChart.as_view(), name='produit-vente-chart'),
    path('dashboard/', chart_view, name='chart1-view'),
    path('api/top-customer-chart/', TopCustomerChart.as_view(), name='top-customer-chart'),
    path('clientchart/', chart_view2, name='chart2-view'),
    path('employe-management/', EmployeManagementView.as_view(), name='employe-management'),
    path('api/absence-chart/', AbsenceChartAPIView.as_view(), name='absence-chart-api'),
    path('absence/', views.absence_create,name='absence'),
    path('avance/', views.paiement, name='avance'),
    path('payroll/', views.liste_employes, name='payroll'),
    path('list_transferts_recu/', views._transferts_, name='list_transferts_recu'),
    path('add_reglement/', add_reglement, name='add_reglement'),
    path('analyse/', views.calculate_total_and_benefit, name='analyse'),
    path('get_client_credit/<int:client_id>/', views.get_client_credit, name='get_client_credit'),
    ##
     #tables urls
    path('tablesManagement/',views.tablesManagement,name='tablesManagementC'),
    #produits CRUD
    path('newProduct/',views.newProduct,name='new productC'),
    path('editProduct/<int:id>',views.editProduct,name='edit productC'),
    path('deleteProduct/<int:id>',views.deleteProduct,name='delete productC'),
    path('searchProduct/',views.searchProduct,name='search productC'),
    #Cient
    path('newClient/',views.newClient,name='new clientC'),
    path('editClient/<int:id>',views.editClient,name='edit clientC'),    
    path('deleteClient/<int:id>',views.deleteClient,name='delete clientC'),
    path('searchClient/',views.searchClient,name='search clientC'),
    #vente
     path('deleteVente/<int:id>',views.deleteVente,name='delete venteC'),
   
]