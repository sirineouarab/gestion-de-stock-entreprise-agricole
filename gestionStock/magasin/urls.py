from django.urls import path
from . import views

urlpatterns = [
    path('tablesManagement/',views.tablesManagement,name='tablesManagement'),
    path('achat/',views.achat,name='achat'),
    path('vente/',views.vente,name='vente'),
    path('transfert/',views.transfert,name='transfert'),
    path('stock/',views.stock,name='stock'),
]