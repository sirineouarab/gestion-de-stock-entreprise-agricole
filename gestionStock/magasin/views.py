from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Produit
from .forms import ProduitForm

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

def newProduct(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProduitForm()
        return redirect('tablesManagement')
    else:
        form = ProduitForm() 
    return render(request,"magasin/addProduct.html",{"form":form})

def deleteProduct(request, id):
    product_delete = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST': 
        product_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/deleteProduct.html",{'produit': product_delete} )
    
def editProduct(request, id):
    product_edit = get_object_or_404(Produit, CodeP=id)
    # form = ProduitForm(instance=produit)
    if request.method=='POST':
        product_save= ProduitForm(request.POST,request.FILES,instance=product_edit)
        if product_save.is_valid():
            product_save.save()
            return redirect('tablesManagement')
    else:
        product_save= ProduitForm(instance=product_edit)
    return render(request,"magasin/editProduct.html",{'produit':product_save})