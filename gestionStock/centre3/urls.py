
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from .views import record_sale,afficher_ventes



urlpatterns = [
    path('sales/', views.record_sale, name='record_sale3'),
    path('liste_ventes/', views.afficher_ventes,name='afficher_vente3'),
    
]
