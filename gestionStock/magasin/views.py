from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def tablesManagement(request):
    return HttpResponse('tables management page')

def achat(request):
    return HttpResponse('achat page')

def transfert(request):
    return HttpResponse('transfert page')

def vente(request):
    return HttpResponse('vente page')

def stock(request):
    return HttpResponse('stock page')