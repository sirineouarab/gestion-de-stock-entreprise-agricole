from django.urls import path
from . import views

urlpatterns = [
    path('tablesManagement/',views.tablesManagement,name='tablesManagement'),
    path('achat/',views.achat,name='achat'),
    path('vente/',views.vente,name='vente'),
    path('transfert/',views.transfert,name='transfert'),
    path('stock/',views.stock,name='stock'),
    path('newProduct/',views.newProduct,name='new product'),
    path('deleteProduct/<int:id>',views.deleteProduct,name='delete product'),
    path('editProduct/<int:id>',views.editProduct,name='edit product'),
    path('searchProduct/',views.searchProduct,name='search product'),
    path('printProducts/',views.printProducts,name='print products'),



]