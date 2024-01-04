from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    


    path('tablesManagement/',views.tablesManagement,name='tablesManagement'),
    path('achat/',views.achat,name='achat'),
    path('achat/<int:id>',views.achatDetails,name='achat details'),
    path('vente/',views.vente,name='vente'),
    path('vente/<int:id>',views.venteDetails,name='vente details'),
    path('transfert/',views.transfert,name='transfert'),
    path('stock/',views.stock,name='stock'),


    path('newProduct/',views.newProduct,name='new product'),
    path('newClient/',views.newClient,name='new client'),
    path('newFournisseur/',views.newFournisseur,name='new fournisseur'),
    path('newCentre/',views.newCentre,name='new centre'),
    path('newEmploye/',views.newEmploye,name='new employe'),
    path('newAchat/',views.newAchat,name='new achat'),
    path('newTransfert/',views.newTransfert,name='new transfert'),
    path('newVente/',views.newVente,name='new vente'),
    path('newProductStock/',views.newProductStock,name='new product stock'),






    path('deleteProduct/<int:id>',views.deleteProduct,name='delete product'),
    path('deleteClient/<int:id>',views.deleteClient,name='delete client'),
    path('deleteFournisseur/<int:id>',views.deleteFournisseur,name='delete fournisseur'),
    path('deleteCentre/<int:id>',views.deleteCentre,name='delete centre'),
    path('deleteEmploye/<int:id>',views.deleteEmploye,name='delete employe'),
    path('deleteTransfert/<int:id>',views.deleteTransfert,name='delete transfert'),
    path('deleteAchat/<int:id>',views.deleteAchat,name='delete achat'),
    path('deleteVente/<int:id>',views.deleteVente,name='delete vente'),
    path('deleteProductStock/<int:id>',views.deleteProductStock,name='delete product stock'),






    path('editProduct/<int:id>',views.editProduct,name='edit product'),
    path('editClient/<int:id>',views.editClient,name='edit client'),    
    path('editFournisseur/<int:id>',views.editFournisseur,name='edit fournisseur'),
    path('editCentre/<int:id>',views.editCentre,name='edit centre'),
    path('editEmploye/<int:id>',views.editEmploye,name='edit employe'),
    path('editAchat/<int:id>',views.editAchat,name='edit achat'),
    path('editVente/<int:id>',views.editVente,name='edit vente'),
    path('editProductStock/<int:id>',views.editProductStock,name='edit product stock'),





    path('searchProduct/',views.searchProduct,name='search product'),
    path('searchClient/',views.searchClient,name='search client'),
    path('searchFournisseur/',views.searchFournisseur,name='search fournisseur'),
    path('searchCentre/',views.searchCentre,name='search centre'),
    path('searchEmploye/',views.searchEmploye,name='search employe'),
    path('searchAchatParFournisseur/',views.searchAchatParFournisseur,name='searchAchatParFournisseur'),
    path('searchAchatParDate/',views.searchAchatParDate,name='searchAchatParDate'),
    path('searchTransfert/',views.searchTransfert,name='search transfert'),
    path('searchVenteParClient/',views.searchVenteParClient,name='searchVenteParClient'),
    path('searchVenteParDate/',views.searchVenteParDate,name='searchVenteParDate'),
    path('searchProduitParNom/',views.searchProduitParNom,name='searchProduitParNom'),
    path('searchProduitParFournisseur/',views.searchProduitParFournisseur,name='searchProduitParFournisseur'),
    path('searchProduitParDate/',views.searchProduitParDate,name='searchProduitParDate'),









    path('printProducts/',views.printProducts,name='print products'),
    path('printProductsStock/',views.printProductsStock,name='print products stock'),
    path('printProductsStockDate/<str:debut_date>/<str:fin_date>',views.printProductsStockDate,name='print products stock date'),
    path('printProductsStockFournisseur/<str:query>',views.printProductsStockFournisseur,name='print products stock fournisseur'),
    path('printProductsStockNom/<str:query>',views.printProductsStockNom,name='print products stock nom'),
    path('printClients/',views.printClients,name='print clients'),
    path('printFournisseurs/',views.printFournisseurs,name='print fournisseurs'),
    path('printCentres/',views.printCentres,name='print centres'),
    path('printEmployes/',views.printEmployes,name='print employes'),





    path('reglement/<int:id>',views.completerPayement,name='reglement'),
    path('paiment/<int:id>',views.PayementCreditSection,name='paiement'),



]