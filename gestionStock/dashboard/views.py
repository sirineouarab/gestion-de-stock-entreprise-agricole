from django.shortcuts import render

# Create your views here.

def vente(request):
    return render(request,'dash/vente.html')

def achat(request):
    return render(request,'dash/achat.html')