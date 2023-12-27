from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),


    path('tablesManagement/',views.tablesManagement,name='tablesManagement'),
    path('achat/',views.achat,name='achat'),
    path('achat/<int:id>',views.achatDetails,name='achat details'),
    path('vente/',views.vente,name='vente'),
    path('transfert/',views.transfert,name='transfert'),
    path('stock/',views.stock,name='stock'),


    path('newProduct/',views.newProduct,name='new product'),
    path('newClient/',views.newClient,name='new client'),
    path('newFournisseur/',views.newFournisseur,name='new fournisseur'),
    path('newCentre/',views.newCentre,name='new centre'),
    path('newEmploye/',views.newEmploye,name='new employe'),
    path('newAchat/',views.newAchat,name='new achat'),



    path('deleteProduct/<int:id>',views.deleteProduct,name='delete product'),
    path('deleteClient/<int:id>',views.deleteClient,name='delete client'),
    path('deleteFournisseur/<int:id>',views.deleteFournisseur,name='delete fournisseur'),
    path('deleteCentre/<int:id>',views.deleteCentre,name='delete centre'),
    path('deleteEmploye/<int:id>',views.deleteEmploye,name='delete employe'),
    path('deleteAchat/<int:id>',views.deleteAchat,name='delete achat'),




    path('editProduct/<int:id>',views.editProduct,name='edit product'),
    path('editClient/<int:id>',views.editClient,name='edit client'),    
    path('editFournisseur/<int:id>',views.editFournisseur,name='edit fournisseur'),
    path('editCentre/<int:id>',views.editCentre,name='edit centre'),
    path('editEmploye/<int:id>',views.editEmploye,name='edit employe'),



    path('searchProduct/',views.searchProduct,name='search product'),
    path('searchClient/',views.searchClient,name='search client'),
    path('searchFournisseur/',views.searchFournisseur,name='search fournisseur'),
    path('searchCentre/',views.searchCentre,name='search centre'),
    path('searchEmploye/',views.searchEmploye,name='search employe'),
    path('searchAchatParFournisseur/',views.searchAchatParFournisseur,name='searchAchatParFournisseur'),
    path('searchAchatParDate/',views.searchAchatParDate,name='searchAchatParDate'),





    path('printProducts/',views.printProducts,name='print products'),
    path('printClients/',views.printClients,name='print clients'),
    path('printFournisseurs/',views.printFournisseurs,name='print fournisseurs'),
    path('printCentres/',views.printCentres,name='print centres'),
    path('printEmployes/',views.printEmployes,name='print employes'),





    path('reglement/<int:id>',views.completerPayement,name='reglement'),


]