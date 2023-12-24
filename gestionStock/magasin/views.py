from django.shortcuts import render
from django.http import HttpResponse
from .models import Produit

# Create your views here.

def tablesManagement(request):
    produits = Produit.objects.all()
    return render(request, 'magasin/tablesmanagement.html', {'produits': produits})

def achat(request):
    return HttpResponse('achat page')

def transfert(request):
    return HttpResponse('transfert page')

def vente(request):
    return HttpResponse('vente page')

def stock(request):
    return HttpResponse('stock page')