from django.urls import path
from . import views

urlpatterns = [
    path('tablesManagement/',views.tablesManagement,name='tablesManagement'),
    path('achat/',views.achat,name='achat'),
    path('vente/',views.vente,name='vente'),
    path('transfert/',views.transfert,name='transfert'),
    path('stock/',views.stock,name='stock'),


    path('newProduct/',views.newProduct,name='new product'),
    path('newClient/',views.newClient,name='new client'),
    path('newFournisseur/',views.newFournisseur,name='new fournisseur'),

    path('deleteProduct/<int:id>',views.deleteProduct,name='delete product'),
    path('deleteClient/<int:id>',views.deleteClient,name='delete client'),
    path('deleteFournisseur/<int:id>',views.deleteFournisseur,name='delete fournisseur'),

    path('editProduct/<int:id>',views.editProduct,name='edit product'),
    path('editClient/<int:id>',views.editClient,name='edit client'),    
    path('editFournisseur/<int:id>',views.editFournisseur,name='edit fournisseur'),

    path('searchProduct/',views.searchProduct,name='search product'),
    path('searchClient/',views.searchClient,name='search client'),
    path('searchFournisseur/',views.searchFournisseur,name='search fournisseur'),

    path('printProducts/',views.printProducts,name='print products'),
    path('printClients/',views.printClients,name='print clients'),
    path('printFournisseurs/',views.printFournisseurs,name='print fournisseurs'),





]