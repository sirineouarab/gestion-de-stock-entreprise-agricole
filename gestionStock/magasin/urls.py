from django.urls import path
from . import views

urlpatterns = [
    #index page
    path('', views.index, name='index'),
    

    #tables urls
    path('tablesManagement/',views.tablesManagement,name='tablesManagement'),
    #produits CRUD
    path('newProduct/',views.newProduct,name='new product'),
    path('editProduct/<int:id>',views.editProduct,name='edit product'),
    path('deleteProduct/<int:id>',views.deleteProduct,name='delete product'),
    path('searchProduct/',views.searchProduct,name='search product'),
    path('printProducts/',views.printProducts,name='print products'),
    #clients CRUD
    path('newClient/',views.newClient,name='new client'),
    path('editClient/<int:id>',views.editClient,name='edit client'),    
    path('deleteClient/<int:id>',views.deleteClient,name='delete client'),
    path('searchClient/',views.searchClient,name='search client'),
    path('printClients/',views.printClients,name='print clients'),
    #fournisseur CRUD
    path('newFournisseur/',views.newFournisseur,name='new fournisseur'),
    path('editFournisseur/<int:id>',views.editFournisseur,name='edit fournisseur'),
    path('deleteFournisseur/<int:id>',views.deleteFournisseur,name='delete fournisseur'),
    path('searchFournisseur/',views.searchFournisseur,name='search fournisseur'),
    path('printFournisseurs/',views.printFournisseurs,name='print fournisseurs'),
    #centre CRUD
    path('newCentre/',views.newCentre,name='new centre'),
    path('editCentre/<int:id>',views.editCentre,name='edit centre'),
    path('deleteCentre/<int:id>',views.deleteCentre,name='delete centre'),
    path('searchCentre/',views.searchCentre,name='search centre'),
    path('printCentres/',views.printCentres,name='print centres'),
    #employes CRUD
    path('newEmploye/',views.newEmploye,name='new employe'),
    path('editEmploye/<int:id>',views.editEmploye,name='edit employe'),
    path('deleteEmploye/<int:id>',views.deleteEmploye,name='delete employe'),
    path('searchEmploye/',views.searchEmploye,name='search employe'),
    path('printEmployes/',views.printEmployes,name='print employes'),


    #achat urls
    path('achat/',views.achat,name='achat'),
    path('achat/<int:id>',views.achatDetails,name='achat details'),
    path('newAchat/', views.newAchat, name='new achat'),
    path('newAchat/<int:fournisseur>/', views.newAchatNewFournisseur, name='new achat'),
    path('newFournisseurAchat/',views.newFournisseurAchat,name='new fournisseur achat'),
    path('editAchat/<int:id>',views.editAchat,name='edit achat'),
    path('deleteAchat/<int:id>',views.deleteAchat,name='delete achat'),
    path('searchAchatParFournisseur/',views.searchAchatParFournisseur,name='searchAchatParFournisseur'),
    path('searchAchatParDate/',views.searchAchatParDate,name='searchAchatParDate'),
    path('reglement/<int:id>',views.completerPayement,name='reglement'),


    #vente urls
    path('vente/',views.vente,name='vente'),
    path('vente/<int:id>',views.venteDetails,name='vente details'),
    path('newVente/',views.newVente,name='new vente'),
    path('editVente/<int:id>',views.editVente,name='edit vente'),
    path('deleteVente/<int:id>',views.deleteVente,name='delete vente'),
    path('searchVenteParClient/',views.searchVenteParClient,name='searchVenteParClient'),
    path('searchVenteParDate/',views.searchVenteParDate,name='searchVenteParDate'),
    path('paiment/<int:id>',views.PayementCreditSection,name='paiement'),


    #transfert urls
    path('transfert/',views.transfert,name='transfert'),
    path('newTransfert/',views.newTransfert,name='new transfert'),
    path('deleteTransfert/<int:id>',views.deleteTransfert,name='delete transfert'),
    path('searchTransfert/',views.searchTransfert,name='search transfert'),


    #stock urls
    path('stock/',views.stock,name='stock'),
    path('newProductStock/',views.newProductStock,name='new product stock'),
    path('deleteProductStock/<int:id>',views.deleteProductStock,name='delete product stock'),
    path('editProductStock/<int:id>',views.editProductStock,name='edit product stock'),
    path('searchProduitParNom/',views.searchProduitParNom,name='searchProduitParNom'),
    path('searchProduitParFournisseur/',views.searchProduitParFournisseur,name='searchProduitParFournisseur'),
    path('searchProduitParDate/',views.searchProduitParDate,name='searchProduitParDate'),
    path('printProductsStock/',views.printProductsStock,name='print products stock'),
    path('printProductsStockDate/<str:debut_date>/<str:fin_date>',views.printProductsStockDate,name='print products stock date'),
    path('printProductsStockFournisseur/<str:query>',views.printProductsStockFournisseur,name='print products stock fournisseur'),
    path('printProductsStockNom/<str:query>',views.printProductsStockNom,name='print products stock nom'),

]